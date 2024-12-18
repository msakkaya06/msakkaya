import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AlertifyService } from '../_services/alertify.service';

import { AuthService } from '../_services/auth.service';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { PasswordValidator } from '../_validators/PasswordValidator';

@Component({
  selector: 'user-register',
  templateUrl: './user-register.component.html',
  styleUrls: ['./user-register.component.css']
})
export class UserRegisterComponent implements OnInit {
  registerForm:FormGroup;

  constructor(public authService: AuthService, private router: Router, private alertify: AlertifyService, private formBuilder:FormBuilder) { 
    this.registerForm = this.formBuilder.group(
    {
      email: new FormControl('',
        [
          Validators.required,
          Validators.email
        ]
      ),
      username: new FormControl('', [Validators.required, Validators.minLength(6)]),
      firstname: new FormControl('', Validators.required),
      lastname: new FormControl('', Validators.required),
      password: new FormControl('', [Validators.required, Validators.minLength(6)]),
      confirmPassword: new FormControl('', [Validators.required, Validators.minLength(6)]),
      birthday: new FormControl('', Validators.required)
    },
    {validators:this.PasswordMatch('password',"confirmPassword")}
  );}
  model: any = {}
  
  ngOnInit(): void {
  }
  

  PasswordMatch(password: any, confirmPassword: any): (form: FormGroup) => void {
    return (form: FormGroup) => {
      const passwordControl = form.controls[password];
      const confirmPasswordControl = form.controls[confirmPassword];

      if (confirmPasswordControl.errors && !confirmPasswordControl.errors['PasswordMatch']) { return; }
      if (passwordControl.value !== confirmPasswordControl.value) {
        confirmPasswordControl.setErrors({ PasswordMatch: true });
      }
      else {
        confirmPasswordControl.setErrors(null);
      }

    }
  }
  register() {
    this.authService.register(this.registerForm.value).subscribe(() => {
      this.alertify.success("Kullanıcı Oluşturuldu")
      this.router.navigate(['/members']);
    },
      error => { this.alertify.error(error); });
  }

}
