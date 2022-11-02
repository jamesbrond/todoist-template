import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ReadedFile } from '../drop-area/drop-area.component';
import { PyEelService, StepperService, TemplateService } from '../../services';
import { Subscription } from 'rxjs';

@Component({
  selector: 'td-template-step',
  templateUrl: './template-step.component.html'
})
export class TemplateStepComponent implements OnInit, OnDestroy {
  file?: File;
  s?: Subscription;

  form = new FormGroup({
    template: new FormControl('', [Validators.required])
  });

  constructor(private _stepper: StepperService, private _template: TemplateService, private _router: Router, private pyeel: PyEelService) { }

  ngOnInit(): void {
    this.form.setValue({ template: this._template.template });
    this.file = this._template.file;
    this.s = this.pyeel.getAPIToken().subscribe();
  }

  ngOnDestroy(): void {
      this.s?.unsubscribe();
  }

  get template() {
    return this.form.get("template");
  }

  submit() {
    if (this.form.valid) {
      this._template.template = this.form.get('template')!.value;
      this._router.navigate(this._stepper.next().link);
    }
  }

  reset() {
    this.form.reset();
  }

  parse(file: ReadedFile): void {
    this._template.file = file.file;
    this.form.setValue({ template: file.content! });
    this.submit();
  }

}
