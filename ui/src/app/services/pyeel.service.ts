import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { USE_REAL_EEL } from '../app.module';
import { PlaceHolder } from '../types';
import { ToasterService } from './toaster.service';

@Injectable({
  providedIn: 'root'
})
export class PyEelService {

  private token$ = new BehaviorSubject<string>('')
  private output$ = new BehaviorSubject<string>('')

  constructor(@Inject(USE_REAL_EEL) private hasEel: boolean, private toaster: ToasterService) { }

  getAPIToken(): Observable<string> {
    const token = this.token$.getValue();
    if (!token) {
      this.getEel().get_api_token()()
        .then((x: any) => { this.token$.next(x) })
        .catch((e: any) => this.catchError(e));
    }
    return this.token$.asObservable();
  }

  runScript(templateName: string, template: string, placeHolders: PlaceHolder[], token: string, dryRun: boolean, isUpdate: boolean): Observable<string> {
    this.getEel().run_script(template, this.toObject(placeHolders), token, dryRun, isUpdate)()
      .then((x: any) => this.output$.next(x))
      .catch((e: any) => this.catchError(e));

    return this.output$.asObservable();
  }

  private toObject(placeHolders: PlaceHolder[]): any {
    let placeHoldersObject: any = {};
    placeHolders.forEach(p => placeHoldersObject[p.key] = p.value);
    return placeHoldersObject;
  }

  private getEel() {
    return this.hasEel ? (window as any).eel : new FakeEel();
  }

  private catchError(e: any) {
    this.toaster.error(e.errorText);
    console.error(e.errorText);
    console.error(e.errorTraceback);
  }
}

class FakeEel {
  get_api_token() {
    return this._callback("1234567890abcde01234567890abcdef0123456c");
  }

  run_script(templateName: string, template: string, placeHolders: PlaceHolder[], token: string, dryRun: boolean, isUpdate: boolean) {
    return this._callback("done", 2000);
  }

  private _callback(message: any, delay: number = 1000) {
    return (callback: any) => setTimeout(() => callback(message), delay);
  }
}
