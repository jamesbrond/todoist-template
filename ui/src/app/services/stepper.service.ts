import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { StepperServiceFactory } from '.';
import { Step } from '../types';

@Injectable({
  providedIn: 'root',
  useFactory: StepperServiceFactory
})
export class StepperService {
  private _steps: Step[] = []
  private _steps$ = new BehaviorSubject<Step[]>([])
  private _current = -1;

  constructor(steps: Step[]) {
    this._steps = steps;
    this._current = 0;
    this.update();
  }

  get steps$(): Observable<Step[]> {
    return this._steps$.asObservable();
  }

  add(step: Step): StepperService {
    // do not add step if already exists
    if (!this._steps.some((x) => x.id == step.id)) {
      this._steps.push(step);
    }
    return this;
  }

  active(stepNumber: number): StepperService {
    if (stepNumber < this.size()) {
      // only one step at time can be active
      this._steps.forEach((x, i) => x.active = i === stepNumber);
      this._current = stepNumber;
    }
    return this;
  }

  disable(stepNumber?: number): StepperService {
    if (stepNumber && stepNumber < this.size()) {
      this._steps[stepNumber].disabled = true;
    } else {
      this._steps[this._current].disabled = true;
    }
    return this;
  }

  enable(stepNumber: number): StepperService {
    if (stepNumber < this.size()) {
      this._steps[stepNumber].disabled = false;
    }
    return this;
  }

  toggle(stepNumber: number): StepperService {
    if (stepNumber < this.size()) {
      this._steps[stepNumber].disabled = !this._steps[stepNumber].disabled;
    }
    return this;
  }

  size(): number {
    return this._steps.length;
  }

  update(): void {
    this._steps$.next(this._steps);
  }

  next(): Step {
    let next = this._current + 1;
    this.enable(next).active(next).update();
    return this._steps[next]
  }

  nextNum(): number {
    return this.currentNum() + 1;
  }

  current(): Step {
    return this._steps[this._current];
  }

  currentNum(): number {
    return this._current;
  }

  go(stepNumber: number): Step {
    this.enable(stepNumber).active(stepNumber).update();
    return this._steps[this._current];
  }

}
