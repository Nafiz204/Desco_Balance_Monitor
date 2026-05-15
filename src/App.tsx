import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Zap, 
  Settings, 
  Bell, 
  CheckCircle2, 
  Mail, 
  Github, 
  Terminal,
  Activity,
  ArrowRight,
  ShieldCheck
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState<'status' | 'setup' | 'logs'>('setup');

  const thresholds = [
    { value: 500, status: 'warning', label: 'Initial Alert' },
    { value: 200, status: 'critical', label: 'Secondary Alert' },
    { value: 100, status: 'urgent', label: 'Final Alert' }
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-amber-400 rounded-lg flex items-center justify-center">
              <Zap className="w-5 h-5 text-white fill-amber-400" />
            </div>
            <h1 className="font-bold text-xl tracking-tight">DESCO Monitor</h1>
          </div>
          <div className="flex bg-slate-100 p-1 rounded-lg">
            {(['status', 'setup', 'logs'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${
                  activeTab === tab 
                    ? 'bg-white text-slate-900 shadow-sm' 
                    : 'text-slate-500 hover:text-slate-700'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          {activeTab === 'setup' && (
            <motion.div
              key="setup"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-8"
            >
              <section>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <Settings className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold">System Configuration</h2>
                    <p className="text-slate-500">Follow these steps to activate your automated monitoring</p>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  {/* Step 1: DESCO */}
                  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                      <div className="bg-amber-50 p-3 rounded-xl border border-amber-100">
                        <Terminal className="w-6 h-6 text-amber-600" />
                      </div>
                      <span className="text-xs font-bold bg-amber-100 text-amber-700 px-2 py-1 rounded">STEP 1</span>
                    </div>
                    <h3 className="text-lg font-bold mb-2">DESCO Credentials</h3>
                    <p className="text-slate-600 text-sm mb-4 leading-relaxed">
                      Collect your account identifier. This usually matches the login used on the 
                      <a href="https://prepaid.desco.org.bd/" target="_blank" className="text-blue-500 hover:underline mx-1">DESCO Prepaid Portal</a>.
                    </p>
                    <div className="space-y-2">
                      <div className="bg-slate-50 p-3 rounded-lg border border-slate-100 text-xs font-mono">
                        DESCO_USER: [Meter/Account No]
                        <br />
                        DESCO_PASS: [Password]
                      </div>
                    </div>
                  </div>

                  {/* Step 2: Email */}
                  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                      <div className="bg-purple-50 p-3 rounded-xl border border-purple-100">
                        <Mail className="w-6 h-6 text-purple-600" />
                      </div>
                      <span className="text-xs font-bold bg-purple-100 text-purple-700 px-2 py-1 rounded">STEP 2</span>
                    </div>
                    <h3 className="text-lg font-bold mb-2">Notification Setup</h3>
                    <p className="text-slate-600 text-sm mb-4 leading-relaxed">
                      Configure your Gmail SMTP endpoint. Use a Google "App Password" to allow the 
                      script to send emails securely.
                    </p>
                    <button className="flex items-center gap-2 text-xs font-bold text-purple-600 hover:text-purple-700">
                      Learn how to create App Password <ArrowRight className="w-3 h-3" />
                    </button>
                  </div>

                  {/* Step 3: GitHub Actions */}
                  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow md:col-span-2">
                    <div className="flex justify-between items-start mb-4">
                      <div className="bg-indigo-50 p-3 rounded-xl border border-indigo-100">
                        <Github className="w-6 h-6 text-indigo-600" />
                      </div>
                      <span className="text-xs font-bold bg-indigo-100 text-indigo-700 px-2 py-1 rounded">FINAL STEP</span>
                    </div>
                    <div className="grid md:grid-cols-2 gap-8">
                      <div>
                        <h3 className="text-lg font-bold mb-2">Deploy to GitHub Actions</h3>
                        <p className="text-slate-600 text-sm leading-relaxed mb-4">
                          Fork this repository and add your secrets. The system will automatically 
                          start monitoring every morning at 7:00 AM Bangladesh Time.
                        </p>
                        <div className="space-y-2">
                          <CheckItem label="Created GitHub Secrets" />
                          <CheckItem label="Workflow Dispatch Enabled" />
                          <CheckItem label="Logs directory created" />
                        </div>
                      </div>
                      <div className="bg-slate-900 rounded-xl p-4 text-xs font-mono text-slate-300 overflow-x-auto">
                        <div className="text-slate-500 mb-2"># .github/workflows/check.yml</div>
                        <div className="text-amber-400">on:</div>
                        <div className="pl-4 text-green-400">schedule:</div>
                        <div className="pl-8">- cron: <span className="text-amber-400">'0 1 * * *'</span></div>
                        <div className="text-amber-400 mt-2">jobs:</div>
                        <div className="pl-4 text-green-400">check-balance:</div>
                        <div className="pl-8">runs-on: ubuntu-latest</div>
                      </div>
                    </div>
                  </div>
                </div>
              </section>

              <section className="bg-blue-600 rounded-3xl p-8 text-white relative overflow-hidden shadow-xl shadow-blue-200">
                <div className="relative z-10 max-w-2xl">
                  <h3 className="text-3xl font-bold mb-4">Ready to secure your power supply?</h3>
                  <p className="text-blue-100 mb-6 text-lg">
                    The Python core logic is ready. You just need to connect your accounts to 
                    start receiving alerts before you run out of credit.
                  </p>
                  <div className="flex flex-wrap gap-4">
                    <button className="bg-white text-blue-600 px-6 py-3 rounded-xl font-bold hover:bg-blue-50 transition-colors flex items-center gap-2">
                      <Terminal className="w-5 h-5" />
                      View Python Code
                    </button>
                    <button className="bg-blue-700 text-white px-6 py-3 rounded-xl font-bold hover:bg-blue-800 transition-colors flex items-center gap-2">
                      <ShieldCheck className="w-5 h-5" />
                      Check Security Docs
                    </button>
                  </div>
                </div>
                <div className="absolute top-1/2 -right-20 -translate-y-1/2 w-80 h-80 bg-blue-500 rounded-full blur-3xl opacity-50" />
              </section>
            </motion.div>
          )}

          {activeTab === 'status' && (
            <motion.div
              key="status"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="grid gap-6 md:grid-cols-3"
            >
              {/* Main Balance Card */}
              <div className="md:col-span-2 bg-white rounded-3xl border border-slate-200 p-8 shadow-sm">
                <div className="flex items-center justify-between mb-8">
                  <div className="flex items-center gap-2 font-bold text-slate-500 uppercase tracking-widest text-xs">
                    <Activity className="w-4 h-4" />
                    Real-time Balance Projection
                  </div>
                  <div className="px-3 py-1 rounded-full bg-emerald-50 text-emerald-600 text-xs font-bold border border-emerald-100 flex items-center gap-1">
                    <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
                    LIVE ESTIMATE
                  </div>
                </div>

                <div className="mb-12">
                  <span className="text-6xl font-black text-slate-900 tracking-tighter">1,245.50</span>
                  <span className="text-2xl font-bold text-slate-400 ml-2">BDT</span>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-50 rounded-2xl p-4 border border-slate-100">
                    <div className="text-sm text-slate-500 mb-1">Status</div>
                    <div className="text-lg font-bold text-emerald-600">Healthy Balance</div>
                  </div>
                  <div className="bg-slate-50 rounded-2xl p-4 border border-slate-100">
                    <div className="text-sm text-slate-500 mb-1">Last Update</div>
                    <div className="text-lg font-bold">12:45 PM Today</div>
                  </div>
                </div>
              </div>

              {/* Threshold Tracking */}
              <div className="bg-white rounded-3xl border border-slate-200 p-8 shadow-sm h-fit">
                <h3 className="font-bold flex items-center gap-2 mb-6 text-slate-700">
                  <Bell className="w-5 h-5 text-amber-500" />
                  Alert Thresholds
                </h3>
                <div className="space-y-6">
                  {thresholds.map((t) => (
                    <div key={t.value} className="relative">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-bold text-slate-700">{t.value} BDT</span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${
                          t.status === 'urgent' ? 'bg-red-100 text-red-600' : 
                          t.status === 'critical' ? 'bg-orange-100 text-orange-600' : 
                          'bg-amber-100 text-amber-600'
                        }`}>
                          {t.label}
                        </span>
                      </div>
                      <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                        <div className="h-full bg-slate-300 w-full opacity-20" />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'logs' && (
            <motion.div
              key="logs"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="bg-slate-900 rounded-3xl p-8 text-slate-300 font-mono text-sm shadow-2xl border border-slate-800"
            >
              <div className="flex items-center justify-between mb-6 border-b border-slate-800 pb-4">
                <div className="flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-indigo-400" />
                  <span className="font-bold text-slate-100">System Logs</span>
                </div>
                <div className="text-xs text-slate-500">logs/monitor.log</div>
              </div>
              <div className="space-y-2">
                <LogLine time="2026-05-15 07:00:01" level="INFO" msg="Starting automated balance monitoring check" />
                <LogLine time="2026-05-15 07:00:05" level="INFO" msg="Playwright initialized successfully" />
                <LogLine time="2026-05-15 07:00:12" level="INFO" msg="Navigation to DESCO portal complete" />
                <LogLine time="2026-05-15 07:00:15" level="INFO" msg="Login successful for user: 82******" />
                <LogLine time="2026-05-15 07:00:18" level="SUCCESS" msg="Current Balance fetched: 1245.50 BDT" />
                <LogLine time="2026-05-15 07:00:18" level="INFO" msg="Threshold check complete. No alerts triggered." />
                <LogLine time="2026-05-15 07:00:19" level="INFO" msg="Process finished with exit code 0" />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <footer className="mt-12 border-t border-slate-200 py-8 text-center text-slate-400 text-sm">
        <p>© 2026 DESCO Balance Monitor System • Powered by Python & GitHub Actions</p>
      </footer>
    </div>
  );
}

function CheckItem({ label }: { label: string }) {
  return (
    <div className="flex items-center gap-2 text-sm text-slate-600">
      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
      {label}
    </div>
  );
}

function LogLine({ time, level, msg }: { time: string, level: string, msg: string }) {
  const levelColor = level === 'ERROR' ? 'text-red-400' : level === 'SUCCESS' ? 'text-emerald-400' : 'text-blue-400';
  return (
    <div className="flex gap-4">
      <span className="text-slate-600 whitespace-nowrap">{time}</span>
      <span className={`font-bold w-16 ${levelColor}`}>{level}</span>
      <span className="text-slate-300">{msg}</span>
    </div>
  );
}

