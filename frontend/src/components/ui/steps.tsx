import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const stepsVariants = cva(
  "flex items-center text-sm font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "text-gray-500",
        active: "text-primary font-bold",
        completed: "text-emerald-600",
        current: "text-primary font-bold",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

interface StepsProps extends React.HTMLAttributes<HTMLDivElement> {
  currentStep?: number;
  totalSteps?: number;
}

const Steps = React.forwardRef<HTMLDivElement, StepsProps>(
  ({ currentStep = 1, totalSteps = 1, className, children, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col gap-4 items-center", className)} {...props}>
      <div className="flex w-fit items-center space-x-4">
        {Array.from({ length: totalSteps }).map((_, index) => {
          const stepNumber = index + 1;
          const isCompleted = stepNumber < currentStep;
          const isCurrent = stepNumber === currentStep;

          return (
            <React.Fragment key={stepNumber}>
              <div className={cn(
                "flex items-center justify-center w-8 h-8 rounded-full border",
                isCompleted
                  ? "bg-emerald-600 border-emerald-600 text-white"
                  : isCurrent
                    ? "bg-primary border-primary text-white"
                    : "border-gray-300 text-gray-500"
              )}>
                {isCompleted ? (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  stepNumber
                )}
              </div>
              {index < totalSteps - 1 && (
                <div className={cn(
                  "h-0.5 w-16",
                  stepNumber < currentStep ? "bg-emerald-600" : "bg-gray-300"
                )} />
              )}
            </React.Fragment>
          );
        })}
      </div>

    </div>
  )
);
Steps.displayName = "Steps";

interface StepProps extends React.HTMLAttributes<HTMLDivElement> {
  step: number;
  currentStep: number;
}

const Step = React.forwardRef<HTMLDivElement, StepProps>(
  ({ step, currentStep, className, children, ...props }, ref) => {
    if (step !== currentStep) {
      return null;
    }
    return (
      <div
        ref={ref}
        className={cn("w-full", className)}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Step.displayName = "Step";

export { Steps, Step };