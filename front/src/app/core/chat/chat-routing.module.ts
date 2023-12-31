import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ChatComponent } from './chat.component';
import { ChatDetailComponent } from './chat-detail/chat-detail.component';

const routes: Routes = [
  { path: '', component: ChatComponent },
  {path: ':username', component:ChatDetailComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ChatRoutingModule { }
