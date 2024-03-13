document.addEventListener('DOMContentLoaded', () => {
    if (!window.StimulusModule) {
        console.error('StimulusModule is not defined, using Django fallback');
        const elements = document.querySelectorAll('[data-controller="file-robot-widget"]');
        elements.forEach((element) => {
            const submit = element.getAttribute('data-file-robot-widget-submit');
            const defaultTabId = element.getAttribute('data-file-robot-widget-default-tab-id');
            const defaultToolId = element.getAttribute('data-file-robot-widget-default-tool-id');
            const useBackendTranslations = element.getAttribute('data-file-robot-widget-use-backend-translations') === 'true';
            const language = element.getAttribute('data-file-robot-widget-language');
            const avoidChangesNotSavedAlertOnLeave = element.getAttribute('data-file-robot-widget-avoid-changes-not-saved-alert-on-leave') === 'true';
            const defaultSavedImageQuality = parseInt(element.getAttribute('data-file-robot-widget-default-saved-image-quality'));
            const forceToPngInEllipticalCrop = element.getAttribute('data-file-robot-widget-force-to-png-in-elliptical-crop') === 'true';
            const useCloudImage = element.getAttribute('data-file-robot-widget-use-cloud-image') === 'true';
            const savingPixelRatio = parseInt(element.getAttribute('data-file-robot-widget-saving-pixel-ratio'));
            const previewPixelRatio = parseInt(element.getAttribute('data-file-robot-widget-preview-pixel-ratio'));
            const observePluginContainerSize = element.getAttribute('data-file-robot-widget-observe-plugin-container-size') === 'true';
            const showCanvasOnly = element.getAttribute('data-file-robot-widget-show-canvas-only') === 'true';
            const useZoomPresetsMenu = element.getAttribute('data-file-robot-widget-use-zoom-presets-menu') === 'true';
            const disableZooming = element.getAttribute('data-file-robot-widget-disable-zooming') === 'true';
            const noCrossOrigin = element.getAttribute('data-file-robot-widget-no-cross-origin') === 'true';
            const disableSaveIfNoChanges = element.getAttribute('data-file-robot-widget-disable-save-if-no-changes') === 'true';
            
            const widget = new FileRobotWidget(
                element.id,
                submit,
                {
                    defaultTabIdValue: defaultTabId,
                    defaultToolIdValue: defaultToolId,
                    useBackendTranslations: useBackendTranslations,
                    language: language,
                    avoidChangesNotSavedAlertOnLeave: avoidChangesNotSavedAlertOnLeave,
                    defaultSavedImageQuality: defaultSavedImageQuality,
                    forceToPngInEllipticalCrop: forceToPngInEllipticalCrop,
                    useCloudImage: useCloudImage,
                    savingPixelRatio: savingPixelRatio,
                    previewPixelRatio: previewPixelRatio,
                    observePluginContainerSize: observePluginContainerSize,
                    showCanvasOnly: showCanvasOnly,
                    useZoomPresetsMenu: useZoomPresetsMenu,
                    disableZooming: disableZooming,
                    noCrossOrigin: noCrossOrigin,
                    disableSaveIfNoChanges: disableSaveIfNoChanges,
                }
            );
        });
    } else {
        console.debug('StimulusModule is defined, using Stimulus for FileRobotWidget')
    }
});





class FileRobotWidgetController extends window.StimulusModule.Controller {
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
    };

    connect() {

        const form = $(this.element).closest('form');
        form.on('submit', () => {
            
        });

        this.widget = new FileRobotWidget(
            this.element.id,
            this.submitValue,
            {
                defaultTabIdValue: this.defaultTabIdValue,
                defaultToolIdValue: this.defaultToolIdValue,
                useBackendTranslations: this.useBackendTranslationsValue,
                language: this.languageValue,
                avoidChangesNotSavedAlertOnLeave: this.avoidChangesNotSavedAlertOnLeaveValue,
                defaultSavedImageQuality: this.defaultSavedImageQualityValue,
                forceToPngInEllipticalCrop: this.forceToPngInEllipticalCropValue,
                useCloudImage: this.useCloudImageValue,
                savingPixelRatio: this.savingPixelRatioValue,
                previewPixelRatio: this.previewPixelRatioValue,
                observePluginContainerSize: this.observePluginContainerSizeValue,
                showCanvasOnly: this.showCanvasOnlyValue,
                useZoomPresetsMenu: this.useZoomPresetsMenuValue,
                disableZooming: this.disableZoomingValue,
                noCrossOrigin: this.noCrossOriginValue,
                disableSaveIfNoChanges: this.disableSaveIfNoChangesValue,
            }
        );
    }

    disconnect() {
        this.widget.disconnect();
        this.widget = null;
    }
}

window.wagtail.app.register('file-robot-widget', FileRobotWidgetController);
