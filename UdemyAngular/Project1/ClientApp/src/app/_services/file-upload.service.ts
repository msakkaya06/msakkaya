import { HttpClient, HttpErrorResponse, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, throwError as observableThrowError } from "rxjs";
import { catchError, map } from "rxjs/operators";
import { Ticket } from "../_models/image";




@Injectable({
  providedIn: 'root'
})
export class UploadFileSimpleService {
  private baseUrl = "http://localhost:5000/api/photos/Add";

  constructor(private http: HttpClient) { }

  postTicket(ticket: Ticket, filesList: FileList): Observable<any> {
    if (!filesList || filesList.length === 0) {
      return observableThrowError("Please select a file.");
    }

    const formData: FormData = new FormData();

    for (const key in ticket) {
      if (ticket.hasOwnProperty(key)) {
        formData.append(key, (<any>ticket)[key]);
      }
    }

    for (let i = 0; i < filesList.length; i++) {
      formData.append(filesList[i].name, filesList[i]);
    }

    const headers = new HttpHeaders().set("Accept", "application/json");
    return this.http
      .post(`${this.baseUrl}`, formData, { headers: headers })
      .pipe(
        map(response => response || {}),
        catchError((error: HttpErrorResponse) => {
          console.error("observable error: ", error);
          return observableThrowError(error);
        }));
  }
}
