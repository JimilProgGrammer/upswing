import { ChartDataSets } from 'chart.js';
import { ApiCallerService } from './../services/api-caller.service';
import { Component, OnInit, Input, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-one-year-chart',
  providers: [ ApiCallerService ],
  templateUrl: './one-year-chart.component.html',
  styleUrls: ['./one-year-chart.component.css']
})
export class OneYearChartComponent implements OnInit {

  @Input() name: String;
  public symbol: String;
  public lineChartData: ChartDataSets[];
  public lineChartLabels: Array<any>;
  loaded = false;

  constructor(private apiCallerService: ApiCallerService) { }

  ngOnInit() {
  }

  // tslint:disable-next-line: use-life-cycle-interface
  ngOnChanges(changes: SimpleChanges) {
    this.loaded = false;
    console.log(JSON.stringify(changes));
    this.symbol = changes.name.currentValue;
    console.log('Current Value --> ', this.symbol);
    this.apiCallerService.doGetRequest('/get_chart_data/' + this.symbol).subscribe(
      res => {
        if (res.data.error == null) {
          this.lineChartLabels = res.data.data.date;
          this.lineChartData = [
            { data: res.data.data.close, label: 'Close'}
          ];
          this.lineChartData = this.lineChartData.slice();
          console.log(this.lineChartLabels);
          this.loaded = true;
        }
      }
    );
  }

  // tslint:disable-next-line: member-ordering
  public lineChartOptions: any = {
    responsive: true,
  };

  // tslint:disable-next-line: member-ordering
  public lineChartColors: Array<any> = [
    { // grey
      backgroundColor: 'rgba(131, 201, 174, 0.2)',
      borderColor: 'rgba(131, 201, 174, 1)',
      pointBackgroundColor: 'rgba(131, 201, 174, 1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(131, 201, 174, 0.8)'
    },
    { // dark grey
      backgroundColor: 'rgba(207, 125, 147, 0.2)',
      borderColor: 'rgba(207, 125, 147, 1)',
      pointBackgroundColor: 'rgba(207, 125, 147, 1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(207, 125, 147, 1)'
    }
  ];
  // tslint:disable-next-line: member-ordering
  public lineChartLegend = true;
  // tslint:disable-next-line: member-ordering
  public lineChartType = 'line';

  // events
  public chartClicked(e: any): void {
    console.log(e);
  }
 
  public chartHovered(e: any): void {
    console.log(e);
  }

}
