// https://github.com/Johann-S/bs-stepper

import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { StepperService } from '../services';
import { Step } from '../types';

@Component({
  selector: 'td-progressbar',
  templateUrl: './progressbar.component.html',
  styleUrls: ['./progressbar.component.scss']
})
export class ProgressbarComponent implements OnInit, OnDestroy {
  steps$: Step[] = []
  s?: Subscription;

  constructor(private _stepper: StepperService, private _router: Router) { }

  ngOnInit(): void {
    this.s = this._stepper.steps$.subscribe((steps) => {
      this.steps$ = steps;
    })
  }

  ngOnDestroy(): void {
    this.s?.unsubscribe();
  }

  go(stepNumber: number) {
    this._router.navigate(this._stepper.go(stepNumber).link);
  }
}
