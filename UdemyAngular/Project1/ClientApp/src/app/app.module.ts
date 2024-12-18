import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { JwtModule } from "@auth0/angular-jwt";
import { AppComponent } from './app.component';
import { NavMenuComponent } from './nav-menu/nav-menu.component';
import { HomeComponent } from './home/home.component';
import { CounterComponent } from './counter/counter.component';
import { FetchDataComponent } from './fetch-data/fetch-data.component';
import { NavbarComponent } from './navbar/navbar.component';
import { UsersComponent } from './users/users.component';
import { UserFormComponent } from './user-form/user-form.component';
import { UserDetailComponent } from './user-detail/user-detail.component';
import { UserRegisterComponent } from './user-register/user-register.component';
import { MemberListComponent } from './members/member-list/member-list.component';
import { FriendListComponent } from './friend-list/friend-list.component';
import { MessagesComponent } from './messages/messages.component';
import { NOTFOUND } from 'dns';
import { NotfoundComponent } from './notfound/notfound.component';
import { appRoutes } from './routes';
import { AuthGuard } from './_guards/auth-guards';
import { ErrorInterceptor } from './_services/error.interceptor';
import { MemberDetailsComponent } from './members/member-details/member-details.component';
import { PhotoComponent } from './photo-gallery/photo.component';
import { ImageUploadComponent } from './image-upload/image-upload.component';
import { CreateActivityComponent } from './create-activity/create-activity.component';
import { UserDetailResolver } from './_resolver/user-detail-resolver';
import { MemberDetailsResolver } from './_resolver/member-details.resolver';
import { ModalCreateMessagesComponent } from './messages/modal-create-messages/modal-create-messages.component';
import { ModalModule } from './_modal';
import { FileUploadModule } from 'ng2-file-upload';
import { ProfilePageComponent } from './profile-page/profile-page.component';
import { CreatePostComponent } from './create-post/create-post.component';
import { ActivityDashboardComponent } from './activity-dashboard/activity-dashboard.component';


export function tokenGetter() {
  return localStorage.getItem("access_token");
}

@NgModule({
  declarations: [
    AppComponent,
    NavMenuComponent,
    HomeComponent,
    CounterComponent,
    FetchDataComponent,
    NavbarComponent,
    MemberListComponent,
    FriendListComponent,
    MessagesComponent,
    MemberDetailsComponent,
    NotfoundComponent,
    PhotoComponent,
    ImageUploadComponent,
    CreateActivityComponent,
    ModalCreateMessagesComponent,
    ProfilePageComponent,
    CreatePostComponent,
    ActivityDashboardComponent,
    UsersComponent,
         UserFormComponent,
         UserDetailComponent,
         UserRegisterComponent
  ],
  imports: [
    BrowserModule.withServerTransition({ appId: 'ng-cli-universal' }),
    HttpClientModule,
    FormsModule,
    FileUploadModule,
    ModalModule,
    JwtModule.forRoot({
      config: {
        tokenGetter: tokenGetter,
        allowedDomains: ["example.com"],
        disallowedRoutes: ["http://example.com/examplebadroute/"],
      },
    }),
    RouterModule.forRoot(appRoutes),
    ReactiveFormsModule
  ],
  providers: [AuthGuard, {
    provide: HTTP_INTERCEPTORS,
    useClass: ErrorInterceptor,
    multi: true
  },
  UserDetailResolver,
  MemberDetailsResolver
],

  bootstrap: [AppComponent]
})
export class AppModule { }
