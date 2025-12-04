import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Chat from "./components/Chat";
import TopMenu from "./components/TopMenu";

import {
  createSession,
  deleteSession,
  getSessions,
} from "./utils/sessionManager";
import Documents from "./pages/Documents";
import FaissInfo from "./pages/FaissInfo";

export default function App() {
  const [sessions, setSessions] = useState<string[]>(() => getSessions());
  const [activeSession, setActiveSession] = useState<string>("");

  useEffect(() => {
    if (sessions.length === 0) {
      const id = createSession();
      setSessions(getSessions());
      setActiveSession(id);
      return;
    }

    if (!sessions.includes(activeSession)) {
      setActiveSession(sessions[0]);
    }

    if (!activeSession) {
      setActiveSession(sessions[0]);
    }
  }, [sessions, activeSession]);

  function handleNewChat() {
    const id = createSession();
    setSessions(getSessions());
    setActiveSession(id);
  }

  function handleDeleteSession(id: string) {
    deleteSession(id);
    const updated = getSessions();
    setSessions(updated);

    if (id === activeSession) {
      if (updated.length > 0) {
        setActiveSession(updated[0]);
      } else {
        const newId = createSession();
        setSessions(getSessions());
        setActiveSession(newId);
      }
    }
  }

  return (
    <BrowserRouter>
      <div className="h-screen flex flex-col bg-neutral-900 text-neutral-100">

        <TopMenu />

        <div className="flex flex-1 overflow-hidden">
          <Routes>

            <Route
              path="/chat"
              element={
                <>
                  <Sidebar
                    sessions={sessions}
                    activeSession={activeSession}
                    onSelect={setActiveSession}
                    onNew={handleNewChat}
                    onDelete={handleDeleteSession}
                  />

                  {activeSession && (
                    <div className="flex-1">
                      <Chat key={activeSession} sessionId={activeSession} />
                    </div>
                  )}
                </>
              }
            />

            <Route path="/documents" element={<Documents />} />
            <Route path="/faiss" element={<FaissInfo />} />

            <Route path="*" element={<Navigate to="/chat" />} />

          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
