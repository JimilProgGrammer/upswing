import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { LogoutComponent } from './logout/logout.component';
import { StockPickerComponent } from './stock-picker/stock-picker.component';
import { PortfolioViewComponent } from './portfolio-view/portfolio-view.component';
import { LeaderboardViewComponent } from './leaderboard-view/leaderboard-view.component';

const routes: Routes = [
  { path:'', pathMatch:'full', redirectTo:'login' },
  { path:'login', component:LoginComponent },
  { path:'signup', component:SignupComponent },
  { path:'logout', component:LogoutComponent },
  { path:'stock_picker', component:StockPickerComponent },
  { path:'view_portfolio', component: PortfolioViewComponent },
  { path:'leaderboard', component: LeaderboardViewComponent }
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
