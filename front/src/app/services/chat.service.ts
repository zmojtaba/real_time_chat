import { Injectable } from '@angular/core';
import {  BehaviorSubject, throwError } from 'rxjs';
import { catchError, map, take, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import {HttpClient, HttpErrorResponse} from "@angular/common/http"
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

interface MessageData {
  message: string;
  time?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private socket$!: WebSocketSubject<any>;
  public receivedData: MessageData[] = [];


  apiUrl              = environment.apiUrl 
  webSockerUrl        = 'ws://127.0.0.1:8000/'
  constructor(private http:HttpClient) {
   }

  connect(): void {
    if (!this.socket$ || this.socket$.closed) {
      this.socket$ = webSocket(this.webSockerUrl+"ws/chat/conversations/moji@gmail.com/");

      this.socket$.subscribe((data: MessageData) => {
        console.log("===============================================================", data)
        this.receivedData.push(data);
      });
    }
  }
  sendMessage(message: string, senderUsername, receiverUsername) {
    this.socket$.next({ message, senderUsername, receiverUsername });
  }

  close() {
    this.socket$.complete();
  }


  conversation(){
    return this.http.get(this.apiUrl+"/chat/conversations/").pipe(
      catchError(this.handleError),
      tap(
        (resData)=>{
        }
      )

    )
  }

  conversationMessages(username){
    return this.http.post(this.apiUrl+"/chat/conversations/"+username+"/", {

    }).pipe(
      catchError(this.handleError),
      tap(data => {
      })
    )
  }











  private handleError(errorRes:HttpErrorResponse){
    let errorMessage = 'an unknown error occurred'
    if (!errorRes.error){
      return throwError(errorMessage)
    }
    if(errorRes.error.error){
      errorMessage=errorRes.error.error['detail']
    }
    if(errorRes.error['username']){
      errorMessage=errorRes.error['username']
    }
    if (errorRes.error['password1']){
      errorMessage=errorRes.error['password1']
    }
    if (errorRes.error['detail']){
      errorMessage=errorRes.error['detail']
    }
    return throwError(errorMessage)
  }
}



