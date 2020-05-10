import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OneYearChartComponent } from './one-year-chart.component';

describe('OneYearChartComponent', () => {
  let component: OneYearChartComponent;
  let fixture: ComponentFixture<OneYearChartComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OneYearChartComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OneYearChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
