import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';

import { AuthGuard } from './_guards/auth-guards';
import { DashboardComponent } from './dashboard/dashboard.component';
import { WebmodulesComponent } from './webmodules/webmodules.component';
import { UserDetailsComponent } from './user-details/user-details.component';


export const appRoutes: Routes = [
  { path: '', component: HomeComponent ,canActivate: [AuthGuard] },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent, canActivate: [AuthGuard] },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'modules', component: WebmodulesComponent},
  { path: 'userdetails', component: UserDetailsComponent, canActivate: [AuthGuard] },



];
