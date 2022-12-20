import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { PlaceHolder } from 'src/app/types';
import { StepperService, TemplateService } from '../../services';

@Component({
  selector: 'td-placeholders-step',
  templateUrl: './placeholders-step.component.html',
  styleUrls: ['./placeholders-step.component.scss']
})
export class PlaceholdersStepComponent implements OnInit, OnDestroy {
  template: string | null = '';
  file?: File;
  form = new FormGroup({});
  controlNames: string[] = [];
  s?: Subscription;

  constructor(private _template: TemplateService, private _stepper: StepperService, private _router: Router) { }

  ngOnInit(): void {
    this.template = this._template.template;
    this.file = this._template.file;
    let placeholders = this._template.placeHolders;
    this._createForm(placeholders);
    if (this.controlNames.length === 0) {
      // disable this step and go to next
      this._router.navigate(this._stepper.disable().next().link);
    } else {
      this._stepper.enable(this._stepper.nextNum());
    }
  }

  ngOnDestroy(): void {
    this.s?.unsubscribe();
    this._setPlaceholder();
  }

  control(name: string) {
    return this.form.get(name);
  }

  reset() {
    this.form.reset();
  }

  submit() {
    if (this.form.valid) {
      this._setPlaceholder();
      this._router.navigate(this._stepper.next().link);
    }
  }

  private _setPlaceholder() {
    let values: PlaceHolder[] = []
    Object.keys(this.form.controls).forEach(x => {
      values.push({ key: x, value: this.form.get(x)!.value });
    });

    this._template.placeHolders = values
  }

  private _createForm(placeHolders: PlaceHolder[]) {
    console.log('placeholders', placeHolders);
    for (let placeHolder of placeHolders) {
      this.controlNames.push(placeHolder.key);
      this.form.addControl(placeHolder.key, new FormControl(placeHolder.value || ''))
    }
  }

}
