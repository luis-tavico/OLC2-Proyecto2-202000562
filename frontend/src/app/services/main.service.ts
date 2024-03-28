import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class MainService {

  private URL = 'http://127.0.0.1:5000/run'

  constructor(private http: HttpClient) { }

  postCode(data: any) {
    return this.http.post(this.URL, data);
  }
  
}