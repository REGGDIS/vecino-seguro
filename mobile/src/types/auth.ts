export interface AuthenticatedUser {
  id: number;
  rut: string;
  fullName: string;
  email: string;
  roleId: number;
}

export interface LoginResponse {
  success: boolean;
  message: string;
  user: AuthenticatedUser;
}
