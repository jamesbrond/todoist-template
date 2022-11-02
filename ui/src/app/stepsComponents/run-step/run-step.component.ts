import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';
import { PyEelService, TemplateService } from '../../services';
import { faBolt } from '@fortawesome/free-solid-svg-icons';
import { PlaceHolder } from 'src/app/types';

@Component({
  selector: 'td-run-step',
  templateUrl: './run-step.component.html',
  styleUrls: ['./run-step.component.scss']
})
export class RunStepComponent implements OnInit, OnDestroy {
  template: string | null = null;
  file?: File;
  placeHolders: PlaceHolder[] = []
  output: string = ''
  hideToken = false;
  renderedTemplate: string | null = null;

  icon_run = faBolt;

  sToken?: Subscription;
  sTodoist?: Subscription;

  form: FormGroup = this.generateForm();

  constructor(private _template: TemplateService, private _py: PyEelService) { }

  ngOnInit(): void {
    this.template = this._template.template;
    this.renderedTemplate = this._template.getRenderedTemplate();
    this.placeHolders = this._template.placeHolders;
    this.file = this._template.file;

    this.sToken = this._py.getAPIToken().subscribe((token) => {
      console.log('subscription "%s"', token, this.hideToken);
      if (token) {
        this.hideToken = true;
        console.log('set token "%s"', token, this.hideToken);
        this.tokenControl?.setValue(token);
        this.tokenControl?.updateValueAndValidity({ onlySelf: false, emitEvent: true });
      }
    });
  }

  ngOnDestroy(): void {
    this.sTodoist?.unsubscribe();
    this.sToken?.unsubscribe();
  }

  get tokenControl() {
    return this.form!.get("token");
  }
  get dryRunControl() {
    return this.form!.get("dryRun");
  }
  get isUpdateControl() {
    return this.form!.get("isUpdate");
  }

  run() {
    this.sTodoist = this._py.runScript(
      this.file?.name || '',
      this.template!,
      this.placeHolders,
      this.tokenControl!.value!,
      this.dryRunControl!.value!,
      this.isUpdateControl!.value!
    ).subscribe(output => this.output = output);
  }

  private generateForm(): FormGroup {
    return new FormGroup({
      token: new FormControl('', [
        Validators.required,
        Validators.minLength(40),
        Validators.maxLength(40)
      ]),
      dryRun: new FormControl(false),
      isUpdate: new FormControl(false)
    });
  }
}
