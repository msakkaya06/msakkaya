import { Routes } from '@angular/router';
import { FriendListComponent } from './friend-list/friend-list.component';
import { HomeComponent } from './home/home.component';
import { MemberDetailsComponent } from './members/member-details/member-details.component';
import { MemberListComponent } from './members/member-list/member-list.component';
import { MessagesComponent } from './messages/messages.component';
import { NotfoundComponent } from './notfound/notfound.component';
import { UserDetailComponent } from './user-detail/user-detail.component';
import { AuthGuard } from './_guards/auth-guards';
import { MemberDetailsResolver } from './_resolver/member-details.resolver';
import { UserDetailResolver } from './_resolver/user-detail-resolver';
import { ProfilePageComponent } from './profile-page/profile-page.component';
import { CreatePostComponent } from './create-post/create-post.component';
import { AdminGuards } from './_guards/admin-guards';

export const appRoutes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'home', component: HomeComponent },
  { path: 'members', component: MemberListComponent, canActivate: [AuthGuard] },
  { path: 'admin', component: MemberListComponent, canActivate: [AdminGuards] },
  { path: 'members/:username', component: MemberDetailsComponent,resolve:{user:MemberDetailsResolver}, canActivate: [AuthGuard] },
  { path: 'profiles/:username', component: ProfilePageComponent,resolve:{user:MemberDetailsResolver}, canActivate: [AuthGuard] },
  { path: 'friends', component: FriendListComponent, canActivate: [AuthGuard] },
  { path: 'messages', component: MessagesComponent, canActivate: [AuthGuard] },
  { path: 'create-post', component: CreatePostComponent, canActivate: [AuthGuard] },
  { path: 'profiles', component: UserDetailComponent,resolve:{user:UserDetailResolver}, canActivate: [AuthGuard] },
  { path: '**', component: NotfoundComponent }


];
