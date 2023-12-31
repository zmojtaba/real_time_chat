import { HttpInterceptor, HttpRequest, HttpHandler } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthInterceptorService implements HttpInterceptor {

  constructor(private authService:AuthService) { }
  intercept(request:HttpRequest<any>, next:HttpHandler){
    if (!localStorage.getItem('refresh_token') || !localStorage.getItem('access_token')){
      console.log("____________________ inteceptor_________________1")

      return next.handle(request)
    }
    const token = localStorage.getItem('access_token')
    console.log("____________________ inteceptor_________________2")
    const modifiedRequest = request.clone({
      setHeaders: {Authorization: `Bearer ${token}`}
    });
    return next.handle(modifiedRequest)
  }
}
