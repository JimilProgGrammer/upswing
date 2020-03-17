import { ApiCallerService } from './../services/api-caller.service';
import { Component, OnInit } from '@angular/core';

import { ChartType, ChartOptions } from 'chart.js';
import { Label } from 'ng2-charts';
import * as pluginDataLabels from 'chartjs-plugin-datalabels';

@Component({
  selector: 'app-portfolio-view',
  providers: [ ApiCallerService ],
  templateUrl: './portfolio-view.component.html',
  styleUrls: ['./portfolio-view.component.css']
})
export class PortfolioViewComponent implements OnInit {

  username: string = "";

  balance: number;
  portfolio_gain: number;
  current_holdings: Array<any>;

  errorMsg: string = "";

  public pieChartOptions: ChartOptions = {
    responsive: true,
    legend: {
      position: 'top',
    },
    plugins: {
      datalabels: {
        formatter: (value, ctx) => {
          const label = ctx.chart.data.labels[ctx.dataIndex];
          return label;
        },
      },
    }
  };
  public pieChartLabels: Label[] = [];
  public pieChartData: number[] = [];
  public pieChartType: ChartType = 'pie';
  public pieChartLegend = true;
  public pieChartPlugins = [pluginDataLabels];
  public pieChartColors = [
    {
      backgroundColor: ['rgba(255,0,0,0.3)', 'rgba(0,255,0,0.3)', 'rgba(0,0,255,0.3)', 'rgba(63, 191, 191, 0.5)',
                        'rgba(135, 34, 235, 0.77)', 'rgba(34, 235, 135, 0.73)', 'rgba(34, 34, 235, 0.63)'],
    },
  ];

  constructor(private _api: ApiCallerService) { }

  ngOnInit() {
    this.username = window.localStorage.getItem("CURRENT_USER_EMAIL")
    this._api.doGetRequest("/get_portfolio/"+this.username).subscribe(res => {
      console.log(res);
      if(res.data.error == null) {
        this.balance = res.data.data.balance;
        this.portfolio_gain = res.data.data.portfolio_net_gain;
        this.current_holdings = res.data.data.current_holdings;
        this.current_holdings.forEach(doc => {
          this.pieChartLabels.push(doc['symbol']);
          this.pieChartData.push(doc['quantity']);
        });
      } else {
        this.errorMsg = res.data.error;
      }
    });
  }

}
