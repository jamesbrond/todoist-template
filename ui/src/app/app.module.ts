import { InjectionToken, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app.routes';
import { AppComponent } from './app.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { NavbarComponent } from './navbar/navbar.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ProgressbarComponent } from './progressbar/progressbar.component';
import { DropAreaComponent, PlaceholdersStepComponent, RunStepComponent, TemplateStepComponent } from './stepsComponents';

import { ReactiveFormsModule } from '@angular/forms';
import { CodePipe } from './pipes';
import { TemplateSourceComponent } from './template-source/template-source.component';
import { environment } from 'src/environments/environment';

export const USE_REAL_EEL = new InjectionToken<boolean>('Use eel.js injected by python Eel');

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    ProgressbarComponent,
    TemplateStepComponent,
    PlaceholdersStepComponent,
    RunStepComponent,
    DropAreaComponent,
    CodePipe,
    TemplateSourceComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FontAwesomeModule,
    NgbModule,
    ReactiveFormsModule,
  ],
  providers: [
      {
        provide: USE_REAL_EEL,
        useValue: environment.production
      }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
