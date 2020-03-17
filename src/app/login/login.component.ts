import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiCallerService } from '../services/api-caller.service';

@Component({
  selector: 'app-login',
  providers: [ ApiCallerService ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  errorMsg: string;
  loginEmail: string;
  loginPwd: string;

  constructor(private auth: ApiCallerService, private router: Router) { }

  ngOnInit() {
  }

  attemptLogin() {
    if(this.loginEmail != null && this.loginEmail.trim() != "" && this.loginPwd != null && this.loginPwd.trim() != "") {
      this.auth.doPostRequest("/auth?username="+this.loginEmail+"&password="+this.loginPwd, {}).subscribe(res => {
        console.log(res);
        window.localStorage.setItem("CURRENT_USER_NAME",res.data.data.name);
        window.localStorage.setItem("CURRENT_USER_EMAIL", this.loginEmail);
        this.router.navigate(['/view_portfolio']);
      });
    } else {
      this.errorMsg = "Username and Password cannot be blank strings.";
    }
  }

}
