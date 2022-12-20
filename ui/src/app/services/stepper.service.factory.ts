import { StepperService } from ".";

export const StepperServiceFactory = () => {
    return new StepperService([
        { id: 'template', title: 'Template', 'link': ['/template'], disabled: false, active: true },
        { id: 'placeholders', title: 'Placeholders', 'link': ['/placeholders'], disabled: true, active: false },
        { id: 'run', title: 'Run', 'link': ['/run'], disabled: true, active: false }
    ]);
}
