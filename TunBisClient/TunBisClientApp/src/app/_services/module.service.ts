import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ModuleService {
  baseUrl: string = "http://localhost:62000/api/module/";

  constructor(private http: HttpClient) { }
  getModulesForUser(userId:string):Observable<any[]>
  {
   
      return this.http.get<any[]>(this.baseUrl + 'GetModulesForUser?userId='+userId);  
  }
}
