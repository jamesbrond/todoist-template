import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PlaceholdersStepComponent, RunStepComponent, TemplateStepComponent } from './stepsComponents';

const routes: Routes = [
  {path: '', redirectTo: '/template', pathMatch: 'full'},
  {path: 'template', component: TemplateStepComponent},
  {path: 'placeholders', component: PlaceholdersStepComponent},
  {path: 'run', component: RunStepComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
