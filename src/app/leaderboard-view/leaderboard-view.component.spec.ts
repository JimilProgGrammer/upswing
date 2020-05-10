import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LeaderboardViewComponent } from './leaderboard-view.component';

describe('LeaderboardViewComponent', () => {
  let component: LeaderboardViewComponent;
  let fixture: ComponentFixture<LeaderboardViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LeaderboardViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LeaderboardViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
