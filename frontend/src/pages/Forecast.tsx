import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Plus, Trash2 } from "lucide-react";

const forecastItemSchema = z.object({
  description: z
    .string()
    .trim()
    .min(1, "Description is required")
    .max(100, "Description must be less than 100 characters"),
  amount: z
    .string()
    .trim()
    .min(1, "Amount is required")
    .refine((val) => !isNaN(Number(val)) && Number(val) > 0, "Amount must be a positive number"),
  frequency: z.enum(["daily", "weekly", "monthly", "quarterly", "annual"]),
});

const forecastSchema = z.object({
  forecastPeriod: z.enum(["30", "60", "90", "180"]),
  expectedInflows: z.array(forecastItemSchema).min(1, "Add at least one income forecast"),
  expectedOutflows: z.array(forecastItemSchema).min(1, "Add at least one expense forecast"),
});

type ForecastForm = z.infer<typeof forecastSchema>;

const Forecast = () => {
  const navigate = useNavigate();
  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
  } = useForm<ForecastForm>({
    resolver: zodResolver(forecastSchema),
    defaultValues: {
      forecastPeriod: "30",
      expectedInflows: [{ description: "", amount: "", frequency: "monthly" }],
      expectedOutflows: [{ description: "", amount: "", frequency: "monthly" }],
    },
  });

  const {
    fields: inflowFields,
    append: appendInflow,
    remove: removeInflow,
  } = useFieldArray({
    control,
    name: "expectedInflows",
  });

  const {
    fields: outflowFields,
    append: appendOutflow,
    remove: removeOutflow,
  } = useFieldArray({
    control,
    name: "expectedOutflows",
  });

  const onSubmit = (data: ForecastForm) => {
    console.log("Forecast data:", {
      ...data,
      expectedInflows: data.expectedInflows.map((item) => ({
        ...item,
        amount: Number(item.amount),
      })),
      expectedOutflows: data.expectedOutflows.map((item) => ({
        ...item,
        amount: Number(item.amount),
      })),
    });
    
    toast.success("Forecast saved successfully!", {
      description: `${data.forecastPeriod}-day cashflow projection has been generated.`,
    });

    // Navigate to results page
    navigate("/forecast/results", {
      state: { forecastPeriod: data.forecastPeriod },
    });
  };

  return (
    <div className="flex-1 space-y-4 p-4 pt-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Cashflow Forecast Input</h2>
          <p className="text-muted-foreground">
            Project your expected income and expenses to generate AI-powered cashflow forecasts.
          </p>
        </div>

        <Card className="p-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
            <div className="space-y-2">
              <Label htmlFor="forecastPeriod">Forecast Period</Label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {["30", "60", "90", "180"].map((days) => (
                  <Button
                    key={days}
                    type="button"
                    variant={watch("forecastPeriod") === days ? "default" : "outline"}
                    onClick={() => setValue("forecastPeriod", days as any)}
                  >
                    {days} Days
                  </Button>
                ))}
              </div>
            </div>

            {/* Expected Inflows */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Expected Income</h3>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => appendInflow({ description: "", amount: "", frequency: "monthly" })}
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Income
                </Button>
              </div>

              {inflowFields.map((field, index) => (
                <Card key={field.id} className="p-4 bg-success/5 border-success/20">
                  <div className="grid md:grid-cols-[2fr_1fr_1fr_auto] gap-3">
                    <div className="space-y-2">
                      <Input
                        placeholder="e.g., Client payments, Product sales"
                        {...register(`expectedInflows.${index}.description`)}
                      />
                      {errors.expectedInflows?.[index]?.description && (
                        <p className="text-xs text-destructive">
                          {errors.expectedInflows[index]?.description?.message}
                        </p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <Input
                        type="number"
                        step="0.01"
                        placeholder="Amount"
                        {...register(`expectedInflows.${index}.amount`)}
                      />
                      {errors.expectedInflows?.[index]?.amount && (
                        <p className="text-xs text-destructive">
                          {errors.expectedInflows[index]?.amount?.message}
                        </p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <select
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                        {...register(`expectedInflows.${index}.frequency`)}
                      >
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                        <option value="quarterly">Quarterly</option>
                        <option value="annual">Annual</option>
                      </select>
                    </div>

                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      onClick={() => removeInflow(index)}
                      disabled={inflowFields.length === 1}
                    >
                      <Trash2 className="w-4 h-4 text-destructive" />
                    </Button>
                  </div>
                </Card>
              ))}
              {errors.expectedInflows?.root && (
                <p className="text-sm text-destructive">{errors.expectedInflows.root.message}</p>
              )}
            </div>

            {/* Expected Outflows */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Expected Expenses</h3>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => appendOutflow({ description: "", amount: "", frequency: "monthly" })}
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Expense
                </Button>
              </div>

              {outflowFields.map((field, index) => (
                <Card key={field.id} className="p-4 bg-destructive/5 border-destructive/20">
                  <div className="grid md:grid-cols-[2fr_1fr_1fr_auto] gap-3">
                    <div className="space-y-2">
                      <Input
                        placeholder="e.g., Rent, Salaries, Supplies"
                        {...register(`expectedOutflows.${index}.description`)}
                      />
                      {errors.expectedOutflows?.[index]?.description && (
                        <p className="text-xs text-destructive">
                          {errors.expectedOutflows[index]?.description?.message}
                        </p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <Input
                        type="number"
                        step="0.01"
                        placeholder="Amount"
                        {...register(`expectedOutflows.${index}.amount`)}
                      />
                      {errors.expectedOutflows?.[index]?.amount && (
                        <p className="text-xs text-destructive">
                          {errors.expectedOutflows[index]?.amount?.message}
                        </p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <select
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                        {...register(`expectedOutflows.${index}.frequency`)}
                      >
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                        <option value="quarterly">Quarterly</option>
                        <option value="annual">Annual</option>
                      </select>
                    </div>

                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      onClick={() => removeOutflow(index)}
                      disabled={outflowFields.length === 1}
                    >
                      <Trash2 className="w-4 h-4 text-destructive" />
                    </Button>
                  </div>
                </Card>
              ))}
              {errors.expectedOutflows?.root && (
                <p className="text-sm text-destructive">{errors.expectedOutflows.root.message}</p>
              )}
            </div>

            <Button type="submit" className="w-full" size="lg">
              Generate AI Forecast
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default Forecast;
