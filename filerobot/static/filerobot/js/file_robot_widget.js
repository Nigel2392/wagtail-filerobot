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
        this.isShowingEditor = false;

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
            // Setting the state in onSave might trigger the onchange.
            // This can mess with scaling. We need to prevent.
            if (this.isShowingEditor) {
                return;
            }
            const widgetState = this.fileInputWidget.widget.getState();
            if (widgetState && widgetState.id) {
                this.constructImageEditor(widgetState);
            }
        }
    }

    _parseDesignState(designState) {
        if (!designState) {
            return;
        }
        // Parse the design state and set it to the editor config if available.
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
                // Set the default saved image name to the source image title.
                this.editorConfig.defaultSavedImageName = sourceImageObj.title;
                this.showImageEditor(data.url);
            } else {
                // Non editable - let wagtail's file input widget handle it.
                delete this.editorConfig
            }
        });
    }

    onSave(editedImageObject, designState) {

        // Get the base64 data from the image and convert it to a file.
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
                    // Set the widget's state.
                    // See onChange in constructFileInput for more info.
                    this.fileInputWidget.widget.setState({
                        id: data.id,
                        title: data.title,
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

        this.isShowingEditor = true;
        this.filerobotImageEditor.render(cpy);

    }

    terminateImageEditor() {
        this.isShowingEditor = false;
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
