import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebmodulesComponent } from './webmodules.component';

describe('WebmodulesComponent', () => {
  let component: WebmodulesComponent;
  let fixture: ComponentFixture<WebmodulesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WebmodulesComponent]
    });
    fixture = TestBed.createComponent(WebmodulesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
