import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { useAuthStore } from '@/stores/auth-store';
import { Eye, EyeOff, Loader2 } from 'lucide-react';
import { Steps, Step } from '@/components/ui/steps';

const MultiStepRegistration: React.FC = () => {
  // Step 1: User registration form data
  const [userFormData, setUserFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
    agreeToTerms: false
  });

  // Step 2: Business registration form data
  const [businessFormData, setBusinessFormData] = useState({
    name: '',
    currency: 'IDR', // Default to Indonesian Rupiah
  });

  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 2;
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const navigate = useNavigate();
  const { register, registerBusiness, isLoading, error, isAuthenticated } = useAuthStore();

  // Check authentication status on component mount
  React.useEffect(() => {
    if (isAuthenticated) {
      // If already authenticated, skip to business registration step
      setCurrentStep(2);
    }
  }, [isAuthenticated]);

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

  // Handle business form errors
  const validateBusinessForm = () => {
    const newErrors: Record<string, string> = {};

    if (!businessFormData.name) {
      newErrors.businessName = 'Business name is required';
    }

    if (!businessFormData.currency) {
      newErrors.currency = 'Currency is required';
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
        setCurrentStep(2);
      }
    } catch (err) {
      console.error("Registration error:", err);
      // Error is handled by the auth store, it will be displayed automatically
    }
  };

  // Handle business registration
  const handleBusinessSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateBusinessForm()) {
      return;
    }

    try {
      // Register the business using the authenticated user's ID
      await registerBusiness({
        name: businessFormData.name,
        currency: businessFormData.currency,
      });

      // After successful business registration, navigate to login
      // This follows the required flow: register user -> register business -> login -> save token to cookie
      navigate('/login');
    } catch (error) {
      console.error('Business registration error:', error);
      setErrors({ businessName: error instanceof Error ? error.message : 'Business registration failed' });
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

  // Handle business form changes
  const handleBusinessChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setBusinessFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleCurrencyChange = (value: string) => {
    setBusinessFormData(prev => ({ ...prev, currency: value }));
  };

  // Previous step
  const goToPreviousStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
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
            <CardTitle className="text-2xl font-bold text-center">
              {currentStep === 1 ? 'User Registration' : 'Business Registration'}
            </CardTitle>
            <CardDescription className="text-center">
              {currentStep === 1 
                ? 'Fill in your personal information to get started' 
                : 'Add your business details'}
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
                    <p className="text-sm text-destructive">{errors.name}</p>
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
                    <p className="text-sm text-destructive">{errors.email}</p>
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
                    <p className="text-sm text-destructive">{errors.password}</p>
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
                    <p className="text-sm text-destructive">{errors.confirmPassword}</p>
                  )}
                </div>

                <div className="flex items-start space-x-2">
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

              <CardFooter className="flex justify-between">
                <div></div> {/* Empty div to push next button to the right */}
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
                    'Continue to Business'
                  )}
                </Button>
              </CardFooter>
            </form>
          </Step>

          {/* Step 2: Business Registration */}
          <Step step={2} currentStep={currentStep}>
            <form onSubmit={handleBusinessSubmit}>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="businessName">Business Name</Label>
                  <Input
                    id="businessName"
                    name="name"
                    type="text"
                    value={businessFormData.name}
                    onChange={handleBusinessChange}
                    placeholder="Enter your business name"
                    className={errors.businessName ? 'border-red-500' : ''}
                  />
                  {errors.businessName && (
                    <p className="text-sm text-destructive">{errors.businessName}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="currency">Currency</Label>
                  <Select value={businessFormData.currency} onValueChange={handleCurrencyChange}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select currency" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="IDR">Indonesian Rupiah (IDR)</SelectItem>
                      <SelectItem value="USD">US Dollar (USD)</SelectItem>
                      <SelectItem value="EUR">Euro (EUR)</SelectItem>
                      <SelectItem value="GBP">British Pound (GBP)</SelectItem>
                    </SelectContent>
                  </Select>
                  {errors.currency && (
                    <p className="text-sm text-destructive">{errors.currency}</p>
                  )}
                </div>
              </CardContent>

              <CardFooter className="flex justify-between">
                <Button
                  type="button"
                  variant="outline"
                  onClick={goToPreviousStep}
                  disabled={isLoading}
                >
                  Back
                </Button>
                <Button
                  type="submit"
                  className="w-1/2"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Creating business...
                    </>
                  ) : (
                    'Register Business'
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