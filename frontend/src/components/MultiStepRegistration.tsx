import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Steps, Step } from '@/components/ui/steps';
import { useAuthStore } from '@/stores/auth-store';
import { Eye, EyeOff, Loader2 } from 'lucide-react';

const MultiStepRegistration: React.FC = () => {
  // Step 1: User registration form data
  const [userFormData, setUserFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
    agreeToTerms: false
  });

  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 1;
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const navigate = useNavigate();
  const { register, registerBusiness, isLoading, error, isAuthenticated } = useAuthStore();

  // Check authentication status on component mount
  React.useEffect(() => {
    if (isAuthenticated) {
      // If already authenticated, redirect to create business page
      navigate('/create-business');
    }
  }, [isAuthenticated, navigate]);

  // Handle user form errors
  const validateUserForm = () => {
    const newErrors: Record<string, string> = {};

    if (!userFormData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(userFormData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!userFormData.password) {
      newErrors.password = 'Password is required';
    } else if (userFormData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (!userFormData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (userFormData.password !== userFormData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!userFormData.name) {
      newErrors.name = 'Name is required';
    }

    if (!userFormData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms and conditions';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };


  // Handle user registration
  const handleUserSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateUserForm()) {
      return;
    }

    setErrors({});

    try {
      await register({
        email: userFormData.email,
        password: userFormData.password,
        name: userFormData.name
      });

      // Wait briefly to ensure state is updated
      await new Promise(resolve => setTimeout(resolve, 100));

      // Get latest state to check if registration was successful
      const { error: currentError, isAuthenticated } = useAuthStore.getState();

      if (!currentError && isAuthenticated) {
        // Instead of going to step 2, redirect to create business page
        navigate('/create-business');
      }
    } catch (err) {
      console.error("Registration error:", err);
      // Error is handled by the auth store, it will be displayed automatically
    }
  };


  // Handle user form changes
  const handleUserChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setUserFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));

    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };


  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-2xl sm:text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Or{' '}
            <Link to="/login" className="font-medium text-primary hover:text-primary/90">
              sign in to your existing account
            </Link>
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-xl sm:text-2xl font-bold text-center">
              User Registration
            </CardTitle>
            <CardDescription className="text-center text-sm sm:text-base">
              Fill in your personal information to get started
            </CardDescription>
          </CardHeader>

          <CardContent>
            <Steps currentStep={currentStep} totalSteps={totalSteps} className="mb-6" />

            {(error || Object.keys(errors).length > 0) && (
              <Alert variant="destructive" className="mb-4">
                <AlertDescription>
                  {error || Object.values(errors)[0]}
                </AlertDescription>
              </Alert>
            )}
          </CardContent>

          {/* Step 1: User Registration */}
          <Step step={1} currentStep={currentStep}>
            <form onSubmit={handleUserSubmit}>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    name="name"
                    type="text"
                    autoComplete="name"
                    required
                    value={userFormData.name}
                    onChange={handleUserChange}
                    placeholder="Enter your full name"
                    className={errors.name ? 'border-red-500' : ''}
                  />
                  {errors.name && (
                    <p className="text-xs sm:text-sm text-destructive">{errors.name}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email address</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={userFormData.email}
                    onChange={handleUserChange}
                    placeholder="Enter your email"
                    className={errors.email ? 'border-red-500' : ''}
                  />
                  {errors.email && (
                    <p className="text-xs sm:text-sm text-destructive">{errors.email}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <div className="relative">
                    <Input
                      id="password"
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      autoComplete="new-password"
                      required
                      value={userFormData.password}
                      onChange={handleUserChange}
                      placeholder="Create a password"
                      className={errors.password ? 'border-red-500' : ''}
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                  {errors.password && (
                    <p className="text-xs sm:text-sm text-destructive">{errors.password}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm Password</Label>
                  <div className="relative">
                    <Input
                      id="confirmPassword"
                      name="confirmPassword"
                      type={showConfirmPassword ? 'text' : 'password'}
                      autoComplete="new-password"
                      required
                      value={userFormData.confirmPassword}
                      onChange={handleUserChange}
                      placeholder="Confirm your password"
                      className={errors.confirmPassword ? 'border-red-500' : ''}
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    >
                      {showConfirmPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                  {errors.confirmPassword && (
                    <p className="text-xs sm:text-sm text-destructive">{errors.confirmPassword}</p>
                  )}
                </div>

                <div className="flex flex-col sm:flex-row sm:items-start space-y-2 sm:space-y-0 space-x-0 sm:space-x-2">
                  <Checkbox
                    id="agreeToTerms"
                    name="agreeToTerms"
                    checked={userFormData.agreeToTerms}
                    onCheckedChange={(checked) =>
                      setUserFormData(prev => ({ ...prev, agreeToTerms: checked as boolean }))
                    }
                  />
                  <Label htmlFor="agreeToTerms" className="text-sm leading-tight">
                    I agree to the{' '}
                    <Link to="/terms" className="text-primary hover:underline">
                      Terms of Service
                    </Link>{' '}
                    and{' '}
                    <Link to="/privacy" className="text-primary hover:underline">
                      Privacy Policy
                    </Link>
                  </Label>
                </div>
              </CardContent>

              <CardFooter className="flex flex-col space-y-4">
                <Button
                  type="submit"
                  className="w-full"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Creating account...
                    </>
                  ) : (
                    'Create Account'
                  )}
                </Button>
              </CardFooter>
            </form>
          </Step>
        </Card>
      </div>
    </div>
  );
};

export default MultiStepRegistration;