import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ChatRoutingModule } from './chat-routing.module';
import { ChatComponent } from './chat.component';
import { NbCardModule, NbChatModule, NbListModule } from '@nebular/theme';
import { ChatDetailComponent } from './chat-detail/chat-detail.component';
import {MatGridListModule} from '@angular/material/grid-list';
import { NbEvaIconsModule } from '@nebular/eva-icons';
import { NbIconModule } from '@nebular/theme';
import { FormsModule } from '@angular/forms';



@NgModule({
  declarations: [
    ChatComponent,
    ChatDetailComponent
  ],
  imports: [
    CommonModule,
    ChatRoutingModule,
    NbCardModule,
    NbListModule,
    MatGridListModule,
    NbChatModule.forRoot({ messageGoogleMapKey: 'MAP_KEY' }),
    NbEvaIconsModule,
    NbIconModule,
    FormsModule,



  ]
})
export class ChatModule { }
