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

class FileRobotWidget {
    constructor(querySelector, submitUrl, simpleConfig) {
        // URL to fetch and send data from/to.
        this.submitUrl = submitUrl;

        // Initialize elements
        this.fileInputWrapper = document.querySelector(`#${querySelector}-filerobot-widget-wrapper`);
        this.fileInput = this.fileInputWrapper.querySelector(`#${querySelector}`);
        this.fileRobot = this.fileInputWrapper.querySelector(`#${querySelector}-filerobot-widget`);

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
        if (bigCfg.obj_tabs === null) {
            bigCfg.obj_tabs = [
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
        $(document).on('click', '.FIE_root button', function(e) {
            if (this.type !== 'button') {
                e.preventDefault();
                this.type = 'button';
            }
        });


        this.editorConfig = {
            onSave: this.onSave.bind(this),
            onClose: () => {
                // Terminate the editor and ask the user for another file.
                this.terminateImageEditor();
                this.fileInput.value = '';
                this.constructFileInput();
            },
        };

        for (const key in simpleConfig) {
            _set_if_not_null(this.editorConfig, key, simpleConfig[key]);
        }
   
        for (const key in bigCfg) {
            _set_if_not_null(this.editorConfig, key, bigCfg[key]);
        }

        const sourceImageID = this.fileInput.value;
        if (!sourceImageID) {
            this.constructFileInput();
        } else {
            this.constructImageEditor(sourceImageID);
        }
    }

    constructFileInput() {
        this.fileInput.type = 'file';
        this.fileInput.accept = 'image/png, image/jpeg, image/jpg, image/webp';
        this.fileInput.onchange = async () => {
            const file = this.fileInput.files[0];
            const base64 = await getBase64(file);
            this.editorConfig.source = base64
            this.editorConfig.defaultSavedImageName = file.name;
            this.editorConfig.defaultSavedImageType = file.type.split('/')[1];
            this.fileInput.type = 'hidden';

            const formData = new FormData();
            formData.append('file', file);
            formData.append('title', file.name);

            makeRequest(this.submitUrl, 'POST', formData).then(data => {
                if (data.success) {
                    this.fileInput.value = data.id;
                    this.editorConfig.source = data.url;
                    if (data.design_state) {
                        this._parseDesignState(data.design_state);
                    }
                    this.showImageEditor();
                    // $(this.fileIn)
                } else {
                    const errors = data.errors;
                    for (const error in errors) {
                        console.error(`Failed to save image on upload (${error}): ${errors[error]}`);
                    }
                }
            });
        }
    }

    _parseDesignState(designState) {
        try {
            this.editorConfig.loadableDesignState = JSON.parse(designState);
            console.log('Design state:', this.editorConfig.loadableDesignState);
        } catch (error) {
            console.error(`Failed to parse design state: ${error.message}`);
        }
    }

    constructImageEditor(sourceImageID) {
        this.fileInput.type = 'hidden';
        return makeRequest(this.submitUrl, 'GET', { image_id: sourceImageID }).then(data => {
            if (data.editable) {
                this.fileInput.value = data.id;
                this.editorConfig.source = data.url;
                if (data.design_state) {
                    this._parseDesignState(data.design_state);
                }
                this.showImageEditor();
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
        formData.append('file', file);
        formData.append('title', editedImageObject.name);
        formData.append('image_id', this.fileInput.value);
        formData.append('design_state', JSON.stringify(designState));

        const p = new Promise((resolve, reject) => {
            makeRequest(this.submitUrl, 'POST', formData).then(data => {
                if (data.success) {
                    this.fileInput.value = data.id;
                    
                } else {
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

    showImageEditor() {
        if (!this.filerobotImageEditor) {
            this.filerobotImageEditor = new FilerobotImageEditor(
                this.fileRobot,
                this.editorConfig
            );
        }

        this.filerobotImageEditor.render({

        });

    }

    terminateImageEditor() {
        this.filerobotImageEditor.terminate();
    }

    setState(value) {
        
    }

    getState() {

    }

    getValue() {

    }

    focus() {

    }

    disconnect() {

    }
}
