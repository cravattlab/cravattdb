import { RouterModule } from '@angular/router';
import { HomeComponent } from './home.component';

export const routing = RouterModule.forChild([
    { path: '', redirectTo: 'search', pathMatch: 'full' },
    { path: 'search', component: HomeComponent }
]);