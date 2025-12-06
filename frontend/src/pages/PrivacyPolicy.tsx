import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const PrivacyPolicy: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardHeader>
            <div className="flex lg:items-center flex-col-reverse gap-4 lg:gap-0 lg:flex-row lg:justify-between">
              <CardTitle className="text-2xl sm:text-3xl font-bold lg:text-center flex-1 capitalize">
                Privacy policy
              </CardTitle>
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigate(-1)}
                className="w-fit"
              >
                <ArrowLeft className="h-4 w-4" />
                Back
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <section>
              <h2 className="text-xl font-semibold mb-3">1. Information We Collect</h2>
              <p className="text-gray-700 mb-3">
                At Cashflow Forecaster, we collect information you provide directly to us, such as when you create an account, update your profile, or contact us for support. This may include:
              </p>
              <ul className="list-disc pl-6 mb-3 text-gray-700">
                <li>Name and contact information</li>
                <li>Email address and password</li>
                <li>Business information and financial data</li>
                <li>Payment information for premium features</li>
              </ul>
              <p className="text-gray-700">
                We also automatically collect certain information about your interaction with our Service, including IP address, browser type, and usage data.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold mb-3">2. How We Use Your Information</h2>
              <p className="text-gray-700 mb-3">
                We use the information we collect to:
              </p>
              <ul className="list-disc pl-6 mb-3 text-gray-700">
                <li>Provide, maintain, and improve the Cashflow Forecaster service</li>
                <li>Process transactions and send related information</li>
                <li>Send you technical notices, updates, and support messages</li>
                <li>Monitor and analyze trends and usage related to our Service</li>
                <li>Protect against fraudulent or illegal activities</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold mb-3">3. Financial Data Handling</h2>
              <p className="text-gray-700 mb-3">
                We take special care in handling your financial information. All financial data you input into the Cashflow Forecaster system is encrypted both in transit and at rest. We only use your financial data to generate cash flow forecasts and reports that you request. We do not share your financial information with third parties without your consent, except as required by law.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold mb-3">4. Information Sharing and Disclosure</h2>
              <p className="text-gray-700 mb-3">
                We do not sell, trade, or rent your personal information to others. We may share your information with third parties in the following circumstances:
              </p>
              <ul className="list-disc pl-6 mb-3 text-gray-700">
                <li>With your consent</li>
                <li>To comply with legal obligations</li>
                <li>To protect the rights, property, or safety of Cashflow Forecaster or others</li>
                <li>With service providers who help us operate our business</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold mb-3">5. Data Security</h2>
              <p className="text-gray-700 mb-3">
                We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. However, no method of transmission over the internet or method of electronic storage is 100% secure, and we cannot guarantee absolute security.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold mb-3">6. Data Retention</h2>
              <p className="text-gray-700 mb-3">
                We retain your personal information for as long as necessary to provide our services and comply with legal obligations. If you delete your account, we will delete your personal information within 30 days, though some information may be retained for legal or business purposes.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold mb-3">7. Your Rights</h2>
              <p className="text-gray-700 mb-3">
                Depending on your location, you may have the right to:
              </p>
              <ul className="list-disc pl-6 mb-3 text-gray-700">
                <li>Access the personal information we hold about you</li>
                <li>Request correction of inaccurate information</li>
                <li>Request deletion of your information</li>
                <li>Object to processing of your information</li>
                <li>Data portability rights</li>
              </ul>
              <p className="text-gray-700">
                To exercise these rights, please contact us at privacy@cashflow-forecaster.com.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold mb-3">8. Children's Privacy</h2>
              <p className="text-gray-700">
                Our Service does not address anyone under the age of 13. We do not knowingly collect personal information from children under 13. If you are a parent or guardian and believe your child has provided us with personal information, please contact us.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold mb-3">9. Changes to This Privacy Policy</h2>
              <p className="text-gray-700 mb-3">
                We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last updated" date.
              </p>
              <p className="text-gray-700">
                You are advised to review this Privacy Policy periodically for any changes. Changes to this Privacy Policy are effective when they are posted on this page.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold mb-3">10. Contact Us</h2>
              <p className="text-gray-700">
                If you have any questions about this Privacy Policy, please contact us at cs@cashflow-forecaster.ryucode.com.
              </p>
            </section>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default PrivacyPolicy;