import { Component, OnInit } from '@angular/core';
import { ModuleService } from '../_services/module.service';
import { AuthService } from '../_services/auth.service.service';
import { LoginComponent } from '../login/login.component';

@Component({
  selector: 'app-webmodules',
  templateUrl: './webmodules.component.html',
  styleUrls: ['./webmodules.component.css']
})
export class WebmodulesComponent {
  modulesList:any[] | undefined;
  userId:string ='';
  constructor(private moduleService:ModuleService,private authService:AuthService){}
  ngOnInit(): void {this.getModulesForUser();
  console.log(this.authService.decodedToken.NameId);}
  getModulesForUser()
    {
      this.moduleService.getModulesForUser(this.authService.decodedToken.NameId).subscribe(modules => { this.modulesList = modules; console.log(this.modulesList)});
   console.log(this.modulesList);
    }

}
