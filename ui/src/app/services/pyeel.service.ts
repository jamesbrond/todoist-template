import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { USE_REAL_EEL } from '../app.module';
import { PlaceHolder } from '../types';

@Injectable({
  providedIn: 'root'
})
export class PyEelService {

  private _token = new BehaviorSubject<string>('')
  private _output = new BehaviorSubject<string>('')

  constructor(@Inject(USE_REAL_EEL) private hasEel: boolean) { }

  getAPIToken(): Observable<string> {
    const token = this._token.getValue();
    if (!token) {
      this.getEel().get_api_token()((x: any) => { console.log('py token',x); this._token.next(x) });
    }
    return this._token.asObservable();
  }

  runScript(templateName: string, template: string, placeHolders: PlaceHolder[], token: string, dryRun: boolean, isUpdate: boolean): Observable<string> {
    this.getEel().run_script(templateName, template, this.toObject(placeHolders), token, dryRun, isUpdate)((x: any) => this._output.next(x));

    return this._output.asObservable();
  }

  private toObject(placeHolders: PlaceHolder[]): any {
    let placeHoldersObject: any = {};
    placeHolders.forEach(p => placeHoldersObject[p.key] = p.value);
    return placeHoldersObject;
  }

  private getEel() {
    return this.hasEel ? (window as any).eel : new FakeEel();
  }
}

class FakeEel {
  get_api_token() {
    return (callback: any) => setTimeout(() => callback("1234567890abcde01234567890abcdef0123456c"), 1000);
  }

  run_script(templateName: string, template: string, placeHolders: PlaceHolder[], token: string, dryRun: boolean, isUpdate: boolean) {
    return (callback: any) => setTimeout(() => callback("ok boomer"), 2000);
  }
}
