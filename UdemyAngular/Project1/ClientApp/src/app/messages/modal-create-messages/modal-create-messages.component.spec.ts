import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalCreateMessagesComponent } from './modal-create-messages.component';

describe('ModalCreateMessagesComponent', () => {
  let component: ModalCreateMessagesComponent;
  let fixture: ComponentFixture<ModalCreateMessagesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ModalCreateMessagesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ModalCreateMessagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
