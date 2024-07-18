import { CircleCheck } from "lucide-react";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { api } from "../../lib/axios";

interface Activity {
  id: string;
  title: string;
  occurs_at: string;
}

export function Activities() {
  const { tripId } = useParams();
  const [activities, setActivities] = useState<Activity[]>([]); 
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const response = await api.get(`/trips/${tripId}/activities`);
        setActivities(response.data.activities); 
        setLoading(false);
      } catch (error) {
        console.error('Erro ao buscar atividades:', error);
        setLoading(false);
      }
    };

    // Chama a função para buscar atividades ao montar o componente
    fetchActivities();
  }, [tripId]);

  return (
    <div className="space-y-8">
      {loading ? (
        <p className="text-zinc-500 text-sm">
          Carregando atividades...
        </p>
      ) : (
        activities.length > 0 ? (
          activities.map(activity => (
            <div key={activity.id} className="space-y-2.5">
              <div className="flex gap-2 items-baseline">
                <span className="text-xl text-zinc-300 font-semibold">
                  Dia {format(new Date(activity.occurs_at), 'd')}
                </span>
                <span className="text-xs text-zinc-500">
                  {format(new Date(activity.occurs_at), 'EEEE', { locale: ptBR })}
                </span>
              </div>
              <div className="px-4 py-2.5 bg-zinc-900 rounded-xl shadow-shape flex items-center gap-3">
                <CircleCheck className="size-5 text-lime-300" />
                <span className="text-zinc-100">{activity.title}</span>
                <span className="text-zinc-400">{format(activity.occurs_at, 'HH:mm')}h</span>
              </div>
            </div>
          ))
        ) : (
          <p className="text-zinc-500 text-sm">
            Nenhuma atividade cadastrada.
          </p>
        )
      )}
    </div>
  );
}
