import { Component, OnInit } from '@angular/core';
import { ApiCallerService } from '../services/api-caller.service';

@Component({
  selector: 'app-leaderboard-view',
  providers: [ ApiCallerService ],
  templateUrl: './leaderboard-view.component.html',
  styleUrls: ['./leaderboard-view.component.css']
})
export class LeaderboardViewComponent implements OnInit {

  current_standings = []
  errorMsg: string;

  constructor(private _api: ApiCallerService) { }

  ngOnInit() {
    this._api.doGetRequest("/get_current_standings").subscribe(res => {
      if(res.data.error == null) {
        console.log(res.data.data);
        this.current_standings = res.data.data;
      } else {
        this.current_standings = res.data.error;
      }
    });
  }

}
