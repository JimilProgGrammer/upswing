import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { ChartsModule } from 'ng2-charts';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { ApiCallerService } from './services/api-caller.service';
import { LoginComponent } from './login/login.component';
import { LogoutComponent } from './logout/logout.component';
import { SignupComponent } from './signup/signup.component';
import { StockPickerComponent } from './stock-picker/stock-picker.component';
import { NavbarComponent } from './navbar/navbar.component';
import { PortfolioViewComponent } from './portfolio-view/portfolio-view.component';
import { LeaderboardViewComponent } from './leaderboard-view/leaderboard-view.component';
import { OneYearChartComponent } from './one-year-chart/one-year-chart.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    LogoutComponent,
    SignupComponent,
    StockPickerComponent,
    NavbarComponent,
    PortfolioViewComponent,
    LeaderboardViewComponent,
    OneYearChartComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    ChartsModule
  ],
  providers: [ ApiCallerService ],
  bootstrap: [AppComponent]
})
export class AppModule { }
