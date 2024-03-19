function base64toBlob(base64Data, contentType) {
    contentType = contentType || '';
    var sliceSize = 1024;
    var byteCharacters = atob(base64Data);
    var bytesLength = byteCharacters.length;
    var slicesCount = Math.ceil(bytesLength / sliceSize);
    var byteArrays = new Array(slicesCount);

    for (var sliceIndex = 0; sliceIndex < slicesCount; ++sliceIndex) {
        var begin = sliceIndex * sliceSize;
        var end = Math.min(begin + sliceSize, bytesLength);

        var bytes = new Array(end - begin);
        for (var offset = begin, i = 0; offset < end; ++i, ++offset) {
            bytes[i] = byteCharacters[offset].charCodeAt(0);
        }
        byteArrays[sliceIndex] = new Uint8Array(bytes);
    }
    return new Blob(byteArrays, { type: contentType });
}


async function getBase64(file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    let p = new Promise((resolve, reject) => {
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
    });
    return p;
}


async function makeRequest(url, method, data = null) {
    const config = {
        method: method,
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
        },
    };

    if (method === 'POST' || method === 'PUT') {
        config.body = data;
    } else if (method === 'GET') {
        try {

            if (url.startsWith('/')) {
                url = window.location.origin + url;
            } else if (!url.startsWith('http')) {
                url = window.location.origin + '/' + url;
            } 

            url = new URL(url);
            Object.keys(data).forEach(key => url.searchParams.append(key, data[key]));
            data = null;
        } catch (error) {
            console.error(`Failed to append query parameters to URL (${url}): ${error.message}`);
        }
    }

    const response = await fetch(url, {
        method: method,
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
        },
        body: data,
    });

    let responseData = response.json();
    if (!response.ok || !response.status === 200) {
        throw new Error(responseData);
    }

    return responseData;
}


function parseJsonScript(querySelector) {
    const script = document.querySelector(querySelector);
    if (script) {
        try{
            return JSON.parse(script.textContent);
        } catch (error) {
            console.error(`Failed to parse JSON from script (${querySelector}): ${error.message}`);
        }
    }
    return null;
}

function _set_if_not_null(obj, key, value) {
    if (value !== null) {
        obj[key] = value;
    }
}


class FilerobotWidget {
    constructor(querySelector, submitUrl, simpleConfig) {
        // URL to fetch and send data from/to.
        this.submitUrl = submitUrl;

        // Initialize elements
        this.fileInputWrapper = document.querySelector(`#${querySelector}-filerobot-widget-wrapper`);
        this.fileInputWidget = this.fileInputWrapper.querySelector(`#${querySelector}-chooser`);
        this.fileRobot = this.fileInputWrapper.querySelector(`#${querySelector}-filerobot-widget`);
        let hasChanged = false;

        const bigCfg = {
            translations:         parseJsonScript('#filerobot-translations'),

            tabsIds:              parseJsonScript(`#${querySelector}-tabs`),
            theme:                parseJsonScript(`#${querySelector}-theme`),
            annotationsCommon:    parseJsonScript(`#${querySelector}-annotationsCommon`),
            Text:                 parseJsonScript(`#${querySelector}-Text`),
            Image:                parseJsonScript(`#${querySelector}-Image`),
            Rect:                 parseJsonScript(`#${querySelector}-Rect`),
            Ellipse:              parseJsonScript(`#${querySelector}-Ellipse`),
            Polygon:              parseJsonScript(`#${querySelector}-Polygon`),
            Pen:                  parseJsonScript(`#${querySelector}-Pen`),
            Line:                 parseJsonScript(`#${querySelector}-Line`),
            Arrow:                parseJsonScript(`#${querySelector}-Arrow`),
            Watermark:            parseJsonScript(`#${querySelector}-Watermark`),
            Rotate:               parseJsonScript(`#${querySelector}-Rotate`),
            Crop:                 parseJsonScript(`#${querySelector}-Crop`),
            CropPresetFolder:     parseJsonScript(`#${querySelector}-CropPresetFolder`),
            CropPresetGroup:      parseJsonScript(`#${querySelector}-CropPresetGroup`),
            CropPresetItem:       parseJsonScript(`#${querySelector}-CropPresetItem`),
            cloudimage:           parseJsonScript(`#${querySelector}-cloudimage`),
        };

        const { TABS, TOOLS } = FilerobotImageEditor;

        // Default tabs if none supplied (all)
        if (bigCfg.tabsIds === null) {
            bigCfg.tabsIds = [
                TABS.ADJUST,
                TABS.FINETUNE,
                TABS.FILTERS,
                TABS.ANNOTATE,
                TABS.RESIZE,
                TABS.WATERMARK,
            ];
        }

        if (simpleConfig.defaultTabId === null) {
            simpleConfig.defaultTabId = TABS[0];
        }

        if (simpleConfig.defaultToolId === null) {
            simpleConfig.defaultToolId = TOOLS[0];
        }

        // Prevent form submission on button click
        // I do not get why the authors of filerobot have not done this.
        $(document).on('click', '.filerobot-widget-container button', function(e) {
            if (this.type != 'button') {
                e.preventDefault();
                this.type = 'button';   
            }
        });

        if (simpleConfig.shouldAutoSave) {
            let isFormSubmit = false;
            $('[data-edit-form] :submit').on('click', (e) => {
                if (isFormSubmit || !hasChanged) {
                    return;
                }

                e.stopImmediatePropagation();
                e.preventDefault();

                isFormSubmit = true;
                const { imageData, designState } = this.filerobotImageEditor.getCurrentImgData();
                this.onSave(imageData, designState).then(data => {
                    if (data.success) {
                        e.currentTarget.click();
                    } else {
                        isFormSubmit = false;
                    }
                });
            });
        } else {
            console.warn(`[FilerobotWidget] Auto save after form submit is disabled for ${querySelector}`);
        }

        this.editorConfig = {
            // removeSaveButton: true,
            disableSaveIfNoChanges: true,
            onSave: this.onSave.bind(this),
            onModify: () => {
                hasChanged = true;
            },
            onClose: (closingReason, haveNotSavedChanges) => {
                // Terminate the editor and ask the user for another file.
                this.terminateImageEditor();
                this.fileInputWidget.widget.setState(null);
                if (this.editorConfig.loadableDesignState) {
                    delete this.editorConfig.loadableDesignState;
                };
                this.constructFileInput();
            },
            // onBeforeSave: (imageFileInfo) => {
            //     let p = new Promise((resolve, reject) => {
            //         const { imageData, designState } = this.filerobotImageEditor.getCurrentImgData()
            //         this.onSave(imageData, designState);
            //         resolve(false);
            //     })
            //     return p;
            // },
            // moreSaveOptions: [
            //     {
            //       label: bigCfg.translations['save'],
            //       icon: '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10.6358 1.52611L10.6367 1.52669C12.0996 2.48423 13.0845 3.97393 13.4308 5.67868C13.7768 7.38223 13.4302 9.13505 12.3952 10.5416L12.39 10.5495C11.4327 12.0121 9.94346 12.9968 8.23923 13.3433C7.8098 13.4238 7.35685 13.4767 6.93362 13.4767C3.87462 13.4767 1.16037 11.323 0.519402 8.23739L0.439941 7.68114V7.66612C0.439941 7.51027 0.483542 7.38547 0.56594 7.28247C0.641164 7.18844 0.75786 7.12545 0.882464 7.10167C1.03156 7.10432 1.15179 7.14773 1.25156 7.22754C1.34816 7.30483 1.41201 7.4259 1.43422 7.55435C1.60415 8.96178 2.28062 10.2289 3.35006 11.1576L3.35104 11.1584C5.69121 13.1603 9.21628 12.8792 11.1914 10.5379C13.1928 8.19761 12.9116 4.67271 10.5702 2.6978C9.44164 1.73866 8.00291 1.28774 6.53782 1.40044L6.53642 1.40056C5.21046 1.51341 3.97038 2.10561 3.04061 3.03539L2.70462 3.37138L3.76055 3.27979L3.7724 3.27705C4.02521 3.21871 4.29448 3.3949 4.35713 3.66641C4.41517 3.91791 4.24109 4.1857 3.97196 4.25015L1.82243 4.62652C1.69199 4.6481 1.55534 4.62267 1.46788 4.5527L1.45879 4.54543L1.4488 4.53944C1.35779 4.48483 1.27678 4.36595 1.25738 4.24958L0.819079 2.08516L0.818029 2.08061C0.759688 1.8278 0.935874 1.55854 1.20739 1.49588C1.45905 1.43781 1.72702 1.61214 1.79125 1.88157L1.96243 2.82299L2.19817 2.56396C4.3538 0.195428 7.94737 -0.257315 10.6358 1.52611Z" fill="#5D6D7E"/><path d="M7.49822 3.76409V7.16923L9.24296 8.91397C9.32292 8.99394 9.38351 9.11495 9.38351 9.25603C9.38351 9.37909 9.3437 9.49734 9.24296 9.59809C9.16576 9.67528 9.0184 9.73864 8.9009 9.73864C8.77784 9.73864 8.65958 9.69883 8.55884 9.59809L6.67355 7.7128C6.59636 7.6356 6.533 7.48823 6.533 7.37074V3.76409C6.533 3.50452 6.75603 3.28148 7.0156 3.28148C7.3025 3.28148 7.49822 3.4772 7.49822 3.76409Z" fill="#5D6D7E"/></svg>',
            //       onClick: (_openSaveModal, saveDirectly) => saveDirectly(console.log),
            //     },
            // ],
        };

        for (const key in simpleConfig) {
            _set_if_not_null(this.editorConfig, key, simpleConfig[key]);
        }
   
        for (const key in bigCfg) {
            _set_if_not_null(this.editorConfig, key, bigCfg[key]);
        }
        
        this.fileInputWidget.widget.input.dataset.tabCount = bigCfg.tabsIds.length;
        const sourceImageObj = this.fileInputWidget.widget.getState();
        if (!sourceImageObj) {
            this.constructFileInput();
        } else {
            this.constructImageEditor(sourceImageObj);
        }
    }

    constructFileInput() {
        this.fileInputWidget.style.display = 'block';
        this.fileInputWidget.widget.input.onchange = async () => {
            const widgetState = this.fileInputWidget.widget.getState();
            if (widgetState && widgetState.id) {
                this.constructImageEditor(widgetState);
            }
        }
    }

    _parseDesignState(designState) {
        try {
            this.editorConfig.loadableDesignState = JSON.parse(designState);
        } catch (error) {
            console.error(`Failed to parse design state: ${error.message}`);
        }
    }

    constructImageEditor(sourceImageObj) {
        this.fileInputWidget.style.display = 'none';
        // Refresh the instance; check if we are allowed to edit.
        return makeRequest(this.submitUrl, 'GET', { image_id: sourceImageObj.id }).then(data => {
            if (data.editable) {
                if (data.design_state) {
                    this._parseDesignState(data.design_state);
                }
                this.showImageEditor(data.url);
            } else {
                let img = document.createElement('img');
                img.src = data.url;
                this.fileRobot.appendChild(img);
                delete this.editorConfig
            }
        });
    }

    onSave(editedImageObject, designState) {
        // data:image/jpec;base64,.....
        const base64Url = editedImageObject.imageBase64;
        const base64Data = base64Url.split(',')[1];
        const blob = base64toBlob(base64Data, 'image/jpeg');
        const file = new File([blob], editedImageObject.fullName, { type: editedImageObject.mimeType });
        const formData = new FormData();
        
        // Even though we let wagtail handle most of the image uploading logic,
        // we still need to save the user-made changes to the image on the server.
        formData.append('file', file);
        formData.append('title', editedImageObject.name);
        formData.append('image_id', this.fileInputWidget.widget.input.value);
        formData.append('design_state', JSON.stringify(designState));

        const p = new Promise((resolve, reject) => {
            makeRequest(this.submitUrl, 'POST', formData).then(data => {
                if (data.success) {
                    this.fileInputWidget.widget.setState({
                        id: data.id,
                        preview: {
                            url: data.url,
                        },
                    });
                } else {

                    if (data.reset) {
                        // Something went terribly wrong; reset the widget.
                        console.error(`Failed to save image: ${data.message}, resetting widget.`);
                        this.fileInputWidget.widget.setState(null);
                        this.constructFileInput();
                        this.terminateImageEditor();
                    }

                    const errors = data.errors;
                    for (const error in errors) {
                        console.error(`Failed to save image (${error}): ${errors[error]}`);
                    }
                }

                resolve(data);
                
            }).catch(error => {
                console.error(`Failed to save image: ${error.message}`);

                reject(error);
            });
        });

        return p;
    }

    showImageEditor(url = null) {
        if (!this.filerobotImageEditor) {
            this.filerobotImageEditor = new FilerobotImageEditor(
                this.fileRobot,
            );
        }


        let cpy = Object.assign({}, this.editorConfig);

        if (url) {
            cpy.source = url;
        }

        this.filerobotImageEditor.render(cpy);

    }

    terminateImageEditor() {
        this.filerobotImageEditor.terminate();
        delete this.filerobotImageEditor;
    }

    setState(value) {
        this.fileInput.value = value;
    }

    getState() {
        return this.fileInput.value;
    }

    getValue() {
        return this.fileInput.value;
    }

    focus() {

    }

    disconnect() {

    }
}
