import React, { useState } from "react";

function Encounters({ encounters }) {
    const [sortKey, setSortKey] = useState("id");
    const [ascending, setAscending] = useState(false);
    const sorted = Object.entries(encounters).sort((a, b) => { // sort the encounters data by specified parameter
        if (sortKey === "id") { // if sorting by name
            return ascending
                ? a[0].localeCompare(b[0])
                : b[0].localeCompare(a[0]);
        }

        let valA, valB;

        if (sortKey === "avg_hp_lost") {
            valA = (a[1].wins + a[1].losses > 0)
                ? a[1].total_hp_lost / (a[1].wins + a[1].losses): 0;

            valB = (b[1].wins + b[1].losses > 0)
                ? b[1].total_hp_lost / (b[1].wins + b[1].losses): 0;
        } else {
            valA = a[1][sortKey] ?? 0;
            valB = b[1][sortKey] ?? 0;
        }

        return ascending ? valA - valB : valB - valA;
    });

    const handleSort = (key) => { // function to handle sort settings for any parameter
        if (sortKey === key) { 
            setAscending(!ascending);
        } else {
            setSortKey(key);
            setAscending(true);
        }
    };

    if (!encounters) return <div>Loading...</div>;

    return (
        <div>
        <h2>Encounters</h2>

        <table border="1" cellPadding="8">
            <thead>
            <tr>
                <th onClick={() => handleSort("id")}>Name</th>
                <th onClick={() => handleSort("winrate")}>Win Rate</th>
                <th onClick={() => handleSort("avg_hp_lost")}>Average HP Lost</th>
            </tr>
            </thead>

            <tbody>
            {sorted.map(([id, encounters]) => (
                <tr key={id}>
                <td>{id}</td>
                <td>{(encounters.winrate * 100).toFixed(1)}%</td>
                <td>{encounters.wins + encounters.losses > 0 ? (encounters.total_hp_lost / (encounters.wins + encounters.losses)).toFixed(1) : "0.0"}</td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>
    );
}

export default Encounters;