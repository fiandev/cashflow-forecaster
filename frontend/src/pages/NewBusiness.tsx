import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import { registerBusiness, updateBusiness, getBusinesses, ApiError, Business } from "@/lib/api";
import { useState } from "react";
import { useAuthStore } from "@/stores/auth-store";
import { useBusiness } from "@/contexts/BusinessContext";
import { useNavigate } from "react-router-dom";

const newBusinessSchema = z.object({
  businessName: z
    .string()
    .trim()
    .min(1, "Business name is required")
    .max(100, "Business name must be less than 100 characters"),
  industry: z
    .string()
    .trim()
    .min(1, "Industry is required")
    .max(50, "Industry must be less than 50 characters"),
  currency: z
    .string()
    .trim()
    .min(1, "Currency is required")
    .max(3, "Currency code must be 3 characters (e.g. USD, EUR)"),
  monthlyRevenue: z
    .string()
    .trim()
    .min(1, "Monthly revenue is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) >= 0, "Must be a valid number"),
  monthlyExpenses: z
    .string()
    .trim()
    .min(1, "Monthly expenses are required")
    .refine((val) => !isNaN(Number(val)) && Number(val) >= 0, "Must be a valid number"),
  currentCash: z
    .string()
    .trim()
    .min(1, "Current cash balance is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) >= 0, "Must be a valid number"),
  outstandingDebt: z
    .string()
    .trim()
    .min(1, "Outstanding debt is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) >= 0, "Must be a valid number"),
  employees: z
    .string()
    .trim()
    .min(1, "Number of employees is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) >= 0 && Number.isInteger(Number(val)), "Must be a whole number"),
  businessGoals: z
    .string()
    .trim()
    .max(500, "Business goals must be less than 500 characters")
    .optional(),
});

type NewBusinessForm = z.infer<typeof newBusinessSchema>;

const NewBusiness = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { user } = useAuthStore();
  const { addBusiness } = useBusiness();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<NewBusinessForm>({
    resolver: zodResolver(newBusinessSchema),
    defaultValues: {
      businessName: "",
      industry: "",
      currency: "USD", // Default currency for new businesses
      monthlyRevenue: "",
      monthlyExpenses: "",
      currentCash: "",
      outstandingDebt: "",
      employees: "",
      businessGoals: "",
    }
  });

  const onSubmit = async (data: NewBusinessForm) => {
    setIsSubmitting(true);

    try {
      // Register the business (basic info only)
      const businessResponse = await registerBusiness({
        name: data.businessName,
        currency: data.currency || "USD", // Use default if not provided
        owner_id: user?.id || 1, // Get user ID from auth store or default to 1
      });

      // Update the business with additional details using settings field
      const fullBusiness = await updateBusiness(businessResponse.id, {
        settings: {
          industry: data.industry,
          monthlyRevenue: Number(data.monthlyRevenue),
          monthlyExpenses: Number(data.monthlyExpenses),
          currentCash: Number(data.currentCash),
          outstandingDebt: Number(data.outstandingDebt),
          employees: Number(data.employees),
          businessGoals: data.businessGoals,
        }
      });

      // Add the new business to the context
      addBusiness(fullBusiness);

      toast.success("Business created successfully!", {
        description: "Your new business has been set up successfully.",
      });

      // Reset the form
      reset();
      
      // Redirect to the main business setup page to view/edit the business
      navigate('/business-setup');
    } catch (error: any) {
      console.error("Error creating business:", error);

      // Check if it's an ApiError with status
      if (error.status) {
        const apiError = error as ApiError;
        switch (apiError.status) {
          case 400:
            toast.error("Validation Error", {
              description: apiError.error || "Invalid data provided. Please check your inputs.",
            });
            break;
          case 401:
            toast.error("Authentication Error", {
              description: apiError.error || "Please log in to continue",
            });
            break;
          case 409:
            toast.error("Conflict Error", {
              description: apiError.error || "A business with this name already exists",
            });
            break;
          case 500:
            toast.error("Server Error", {
              description: apiError.error || "An error occurred on the server. Please try again later.",
            });
            break;
          default:
            toast.error("Request Failed", {
              description: apiError.error || `Error ${apiError.status}: ${apiError.message || 'An error occurred'}`,
            });
        }
      } else {
        // Generic error (not an HTTP error)
        toast.error("Failed to create business", {
          description: error.message || "An unknown error occurred",
        });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex-1 space-y-4 p-4 pt-6">
      <div className="max-w-3xl mx-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Create New Business</h2>
          <p className="text-muted-foreground">
            Set up a new business profile for financial analysis.
          </p>
        </div>

        <Card className="p-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="businessName">Business Name</Label>
                <Input
                  id="businessName"
                  placeholder="Your Business Inc."
                  {...register("businessName")}
                />
                {errors.businessName && (
                  <p className="text-sm text-destructive">{errors.businessName.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="currency">Currency</Label>
                <Input
                  id="currency"
                  placeholder="e.g., USD, EUR, IDR"
                  {...register("currency")}
                />
                {errors.currency && (
                  <p className="text-sm text-destructive">{errors.currency.message}</p>
                )}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="industry">Industry</Label>
                <Input
                  id="industry"
                  placeholder="e.g., Retail, SaaS, Consulting"
                  {...register("industry")}
                />
                {errors.industry && (
                  <p className="text-sm text-destructive">{errors.industry.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="employees">Number of Employees</Label>
                <Input
                  id="employees"
                  type="number"
                  placeholder="10"
                  {...register("employees")}
                />
                {errors.employees && (
                  <p className="text-sm text-destructive">{errors.employees.message}</p>
                )}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="monthlyRevenue">Average Monthly Revenue ($)</Label>
                <Input
                  id="monthlyRevenue"
                  type="number"
                  step="0.01"
                  placeholder="50000"
                  {...register("monthlyRevenue")}
                />
                {errors.monthlyRevenue && (
                  <p className="text-sm text-destructive">{errors.monthlyRevenue.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="monthlyExpenses">Average Monthly Expenses ($)</Label>
                <Input
                  id="monthlyExpenses"
                  type="number"
                  step="0.01"
                  placeholder="35000"
                  {...register("monthlyExpenses")}
                />
                {errors.monthlyExpenses && (
                  <p className="text-sm text-destructive">{errors.monthlyExpenses.message}</p>
                )}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="currentCash">Current Cash Balance ($)</Label>
                <Input
                  id="currentCash"
                  type="number"
                  step="0.01"
                  placeholder="100000"
                  {...register("currentCash")}
                />
                {errors.currentCash && (
                  <p className="text-sm text-destructive">{errors.currentCash.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="outstandingDebt">Outstanding Debt ($)</Label>
                <Input
                  id="outstandingDebt"
                  type="number"
                  step="0.01"
                  placeholder="25000"
                  {...register("outstandingDebt")}
                />
                {errors.outstandingDebt && (
                  <p className="text-sm text-destructive">{errors.outstandingDebt.message}</p>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="businessGoals">Business Goals (Optional)</Label>
              <Textarea
                id="businessGoals"
                placeholder="Describe your short-term and long-term business goals..."
                rows={4}
                {...register("businessGoals")}
              />
              {errors.businessGoals && (
                <p className="text-sm text-destructive">{errors.businessGoals.message}</p>
              )}
            </div>

            <div className="flex gap-4">
              <Button type="submit" className="flex-1" disabled={isSubmitting}>
                {isSubmitting ? "Creating..." : "Create Business"}
              </Button>
              <Button 
                type="button" 
                variant="outline" 
                onClick={() => navigate('/business-setup')}
                disabled={isSubmitting}
              >
                Cancel
              </Button>
            </div>
          </form>
        </Card>

        <Card className="p-6 mt-6 bg-primary/5 border-primary/20">
          <h3 className="font-semibold mb-2 flex items-center gap-2">
            <span className="text-primary">💡</span> Why we need this information
          </h3>
          <p className="text-sm text-muted-foreground">
            This data helps our AI analyze your financial health, predict cashflow patterns,
            and provide personalized risk assessments. All information is encrypted and secure.
          </p>
        </Card>
      </div>
    </div>
  );
};

export default NewBusiness;