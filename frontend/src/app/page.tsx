import UserForm from "@/components/UserForm";

export default function Home() {
  return (
    <div className="relative min-h-screen flex flex-col justify-center">
      <div
        className="absolute inset-0 z-0 bg-cover bg-center opacity-30"
        style={{ backgroundImage: "url('/doctor.png')" }}
      />
      <main className="relative z-10 max-w-2xl mx-auto">
        <UserForm />
      </main>
    </div>
  );
}