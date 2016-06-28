// http://www.wintellect.com/devcenter/dbaskin/yes-used-jquery-angular2-application
import {Directive, ElementRef, OnInit, OnDestroy} from '@angular/core'

declare var $: any

@Directive({ selector: '.ui.dropdown' })
export class InitializeDropdown implements OnInit, OnDestroy {
    constructor(private el: ElementRef) {}

    ngOnInit() {
        $(this.el.nativeElement).dropdown();
    }

    ngOnDestroy() {
        $(this.el.nativeElement).dropdown('destroy');
    }
}

@Directive({ selector: '.ui.checkbox' })
export class InitializeCheckbox implements OnInit, OnDestroy {
    constructor(private el: ElementRef) { }

    ngOnInit() {
        $(this.el.nativeElement).checkbox();
    }

    ngOnDestroy() {
        $(this.el.nativeElement).checkbox('destroy');
    }
}