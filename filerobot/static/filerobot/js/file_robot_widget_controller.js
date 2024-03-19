class FilerobotWidgetController extends window.StimulusModule.Controller {
    static values = { 
        submit: { type: String },
        defaultTabId: { type: String },
        defaultToolId: { type: String },
        useBackendTranslations: { default: true, type: Boolean },
        language: { default: 'en', type: String },
        avoidChangesNotSavedAlertOnLeave: { default: false, type: Boolean },
        defaultSavedImageQuality: { default: 1, type: Number },
        forceToPngInEllipticalCrop: { default: false, type: Boolean },
        useCloudImage: { default: false, type: Boolean },
        savingPixelRatio: { default: 4, type: Number },
        previewPixelRatio: { default: window.devicePixelRatio, type: Number },
        observePluginContainerSize: { default: false, type: Boolean },
        showCanvasOnly: { default: false, type: Boolean },
        useZoomPresetsMenu: { default: true, type: Boolean },
        disableZooming: { default: false, type: Boolean },
        noCrossOrigin: { default: false, type: Boolean },
        disableSaveIfNoChanges: { default: false, type: Boolean },

        // Custom
        shouldAutoSave: { default: true, type: Boolean },
    };

    connect() {

        const form = $(this.element).closest('form');
        form.on('submit', () => {
            
        });

        this.widget = new FilerobotWidget(
            this.element.id,
            this.submitValue,
            {
                defaultTabId:                     this.defaultTabIdValue,
                defaultToolId:                    this.defaultToolIdValue,
                useBackendTranslations:           this.useBackendTranslationsValue,
                language:                         this.languageValue,
                avoidChangesNotSavedAlertOnLeave: this.avoidChangesNotSavedAlertOnLeaveValue,
                defaultSavedImageQuality:         this.defaultSavedImageQualityValue,
                forceToPngInEllipticalCrop:       this.forceToPngInEllipticalCropValue,
                useCloudImage:                    this.useCloudImageValue,
                savingPixelRatio:                 this.savingPixelRatioValue,
                previewPixelRatio:                this.previewPixelRatioValue,
                observePluginContainerSize:       this.observePluginContainerSizeValue,
                showCanvasOnly:                   this.showCanvasOnlyValue,
                useZoomPresetsMenu:               this.useZoomPresetsMenuValue,
                disableZooming:                   this.disableZoomingValue,
                noCrossOrigin:                    this.noCrossOriginValue,
                disableSaveIfNoChanges:           this.disableSaveIfNoChangesValue,
                
                // Custom
                shouldAutoSave:                   this.shouldAutoSaveValue,
            }
        );
    }

    disconnect() {
        this.widget.disconnect();
        this.widget = null;
    }
}

window.wagtail.app.register('file-robot-widget', FilerobotWidgetController);
