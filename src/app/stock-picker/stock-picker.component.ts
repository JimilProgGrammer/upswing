import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ApiCallerService } from '../services/api-caller.service';

@Component({
  selector: 'app-stock-picker',
  providers: [ ApiCallerService ],
  templateUrl: './stock-picker.component.html',
  styleUrls: ['./stock-picker.component.css']
})
export class StockPickerComponent implements OnInit {

  savedLogin: string;
  savedName: string;
  stocks: Array<Object>;
  balance: number;
  selectedStock: string;
  selectedDescription: string;

  successMsg: string;
  errorMsg: string;

  @ViewChild('openModalButton') modalButton:ElementRef;

  constructor(private _api: ApiCallerService) { }

  ngOnInit() {
    this.savedLogin = window.localStorage.getItem("CURRENT_USER_EMAIL");
    this.savedName = window.localStorage.getItem("CURRENT_USER_NAME");
    this._api.doGetRequest("/stock_picker/"+this.savedLogin).subscribe(res => {
      if(res.data.error == null) {
        this.stocks = res.data.data.data;
        console.log(this.stocks);
        this.stocks.forEach(stock_doc => {
          stock_doc['quantity'] = 0;
        });
        this.balance = res.data.data.balance;
      } else {
        console.log(res.data.error);
        this.errorMsg = res.data.error;
      }
    });
  }

  openModal(stock_name: string) {
    this.selectedStock = stock_name;
    this.stocks.forEach(stock_doc => {
      if(stock_doc['stock_name'] == stock_name) {
        this.selectedDescription = stock_doc['description'];
      }
    });
    console.log("Modal triggered: " + stock_name);
    this.modalButton.nativeElement.click();
  }

  performBuy(stock_name: string, price: number, quantity: number) {
    this.successMsg = "";
    this.errorMsg = "";
    this._api.doPostRequest("/buy_stocks?username="+this.savedLogin
      +"&stock_name="+stock_name+"&quantity="+quantity+"&price="+price, {}).subscribe(res => {
        console.log(res);
        if(res.data.error == null) {
          this.successMsg = res.data.data;
          this.balance = this.balance - (price*quantity);
        } else {
          this.errorMsg = res.data.error;
        }
      });
  }

  performSell(stock_name: string, price: number, quantity: number) {
    this.successMsg = "";
    this.errorMsg = "";
    this._api.doPostRequest("/sell_stocks?username="+this.savedLogin
      +"&stock_name="+stock_name+"&quantity="+quantity+"&price="+price, {}).subscribe(res => {
        console.log(res);
        if(res.data.error == null) {
          this.successMsg = res.data.data;
          this.balance = this.balance + (price*quantity);
        } else {
          this.errorMsg = res.data.error;
        }
      });
  }

}
