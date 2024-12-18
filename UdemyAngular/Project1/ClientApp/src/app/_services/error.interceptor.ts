import { HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from "@angular/common/http";

import { catchError, Observable, throwError } from "rxjs";

export class ErrorInterceptor implements HttpInterceptor {
    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
      return next.handle(req)
      .pipe(catchError((error: HttpErrorResponse) => {
        if (error.status === 400) {


          if (error.error.errors) {
            const serverError = error.error;
            let errorMessage = '';
            for (const key in serverError.errors) { errorMessage += serverError.errors[key] + '\n'; }
            return throwError(errorMessage)
          }
          return throwError(error.error);
        }
        if (error.status === 500) { return throwError(error.error.Message); }
        return throwError(error.error);
      }))
    }


}
