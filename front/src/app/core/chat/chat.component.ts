import { Component, OnInit } from '@angular/core';
import { ChatService } from 'src/app/services/chat.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit {
  conversations;

  constructor(
    private chatService: ChatService,
    private router: Router,
  ){
  }
  // we dont know what username is other username to show in the chat room so we specify it here
  findChatUserName(data, username){
    for(let conversation of data){
      if (conversation.starter.username == username){
        conversation.otherUsername = conversation.receiver.username
      }else{
        conversation.otherUsername = conversation.starter.username
      }
      
    }
    return data
  }

  chatUsername
  onChatUsername(event){
    this.chatUsername = event
  }

  ngOnInit() {
    this.chatService.conversation().subscribe( data=>{
      this.conversations = this.findChatUserName(data['detail'], localStorage.getItem('username'))      
    } )
  }

}
