import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { ChatService } from 'src/app/services/chat.service';

@Component({
  selector: 'app-chat-detail',
  templateUrl: './chat-detail.component.html',
  styleUrls: ['./chat-detail.component.scss']
})
export class ChatDetailComponent implements OnInit, OnChanges {

  @Input() otherUsername:string ;
  myUsername=localStorage.getItem('username');

  chatMessages;
  textMessage;

  constructor(private chatService : ChatService) {
    
  }
  // it see the @input and with any changes it change 
  ngOnChanges() {
    if(this.otherUsername){
      this.chatService.conversationMessages(this.otherUsername).subscribe(data=>{
        this.chatMessages = data
        console.log(data)
        
      })
      this.chatService.connect()
    }

  }
  ngOnInit(): void {
  }

  onSendMessage(){
    console.log("_____________________click______________________")
    this.chatService.sendMessage(this.textMessage, this.myUsername, this.otherUsername)
  }

  
  
}
