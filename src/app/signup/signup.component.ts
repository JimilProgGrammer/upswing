import { Component, OnInit } from '@angular/core';
import { ApiCallerService } from '../services/api-caller.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  providers: [ApiCallerService],
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  name: string;
  email_id: string;
  password: string;
  errorMsg: string;
  otp: string;
  savedUsername: string;
  
  constructor(private _api: ApiCallerService, private router: Router) { }

  ngOnInit() {
  }

  doSignUp() {
    if(this.name != null && this.password != null && this.email_id != null) {
        var url = "/signup";
        url += "?name="+this.name;
        url += "&email_id="+this.email_id;
        url += "&password="+this.password;
        console.log(url);
        this._api.doPostRequest(url, {}).subscribe(
          res => {
            if(res.error == null) {
              console.log(res.data);
              this.savedUsername = this.email_id;
              this.name = "";
              this.password = "";
              let element: HTMLElement = document.getElementById('verifyOtp') as HTMLElement;
              element.click();
            } else {
              this.errorMsg = res.error;
            }
          }
        );
    } else {
      this.errorMsg = "Please fill in the required fields."
    }
  }

  verifyOtp() {
    if(this.email_id != null && this.otp != null) {
      var url = "/verify/"+this.savedUsername+"/"+this.otp;
      this._api.doPostRequest(url, {}).subscribe(
        res => {
          let elem: HTMLElement = document.getElementById('dismissModal') as HTMLElement;
          console.log(res);
          if(res.error == null) {
            this.router.navigate(['/login']);
            elem.click();
          } else {
            this.errorMsg = "OTP Verification failed";
          }
        }
      )
    }
  }

}
