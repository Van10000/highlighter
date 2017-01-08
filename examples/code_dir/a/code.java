package Core.Game;
/**
 * Created by Владимир on 16.09.2016.
 */

import Core.GameCommands.GameCommand;
import Core.GameObjects.CatDog;
import Core.GameObjects.GameObject;
import Core.GameObjects.Snake;
import Core.GameUpdatingSystem.GameUpdatingSystem;
import Core.MapObjects.DynamicMapObjects.SnakeCell;
import Core.MapObjects.MapObject;
import Core.MapObjects.StaticMapObjects.Berries.Berry;
import Core.MapObjects.StaticMapObjects.EmptyCell;
import Core.MapObjects.StaticMapObjects.Wall;
import Core.Utils.IntPair;

import java.io.*;
import java.util.ArrayList;

public class Game extends AbstractGame implements Serializable, Cloneable
{
    public ArrayList<GameObject> gameObjects;
    private GameUpdatingSystem gameUpdatingSystem;
    private MapObject[][] map;

    public boolean isFinished()
    {
        return gameObjects.stream().anyMatch(GameObject::getIsDestructed);
    } // TODO: let gameUpdatingSystem decide when game finishes

    public Game(MapObject[][] map, ArrayList<GameObject> gameObjects, GameUpdatingSystem gameUpdatingSystem)
    {
        this.map = map;
        this.gameObjects = gameObjects;
        this.gameUpdatingSystem = gameUpdatingSystem;
    }

    public void executeCommand(GameCommand command)
    {
        command.execute(this);
    }

    public MapObject[][] getCurrentMap()
    {
        return map;
    }
    public void setCurrentMap(MapObject[][] map)
    {
        this.map = map;
    }

    @Override
    public ArrayList<GameObject> getGameObjects()
    {
        return gameObjects;
    }

    @Override
    public Game clone()
    {
        try
        {
            return (Game) super.clone();
        }
        catch (CloneNotSupportedException e)
        {
            throw new InternalError();
        }
    }

    public void update()
    {
        if (isFinished())
            throw new UnsupportedOperationException("Game finished. Impossible to update.");
        gameUpdatingSystem.updateGame(this);
    }

    public static Game loadGame(String filePath) throws IOException, ClassNotFoundException
    {
        try (FileInputStream stream = new FileInputStream(filePath))
        {
            return loadGame(stream);
        }
    }

    public static Game loadGame(FileInputStream fileInputStream) throws IOException, ClassNotFoundException
    {
        try (ObjectInputStream stream = new ObjectInputStream(fileInputStream))
        {
            return loadGame(stream);
        }
    }

    public static Game loadGame(ObjectInputStream objectInputStream) throws IOException, ClassNotFoundException
    {
        return (Game)objectInputStream.readObject();
    }

    public void writeGame(String filePath) throws IOException, ClassNotFoundException
    {
        try (FileOutputStream stream = new FileOutputStream(filePath))
        {
            writeGame(stream);
        }
    }

    public void writeGame(FileOutputStream fileOutputStream) throws IOException, ClassNotFoundException
    {
        try (ObjectOutputStream stream = new ObjectOutputStream(fileOutputStream))
        {
            writeGame(stream);
        }
    }

    public void writeGame(ObjectOutputStream objectInputStream) throws IOException, ClassNotFoundException
    {
        objectInputStream.writeObject(this);
    }

    public int getAliveSnakeIndex()
    {
        GameObject[] snakes = gameObjects.stream()
                .filter(gameObject -> gameObject instanceof Snake)
                .toArray(GameObject[]::new);
        for(int i = 0; i < snakes.length; ++i)
            if (!snakes[i].getIsDestructed())
                return i;
        return -1;
    }

    public MapObject getCellAt(IntPair coordinates)
    {
        return getCurrentMap()[coordinates.x][coordinates.y];
    }

    @Override
    public String toString()
    {
        StringBuilder builder = new StringBuilder();
        MapObject[][] map = getCurrentMap();

        for (int i = 0; i < getWidth(); ++i)
        {
            for (int j = 0; j < getHeight(); ++j)
                if (map[i][j] instanceof Wall)
                    builder.append('#');
                else if (map[i][j] instanceof EmptyCell)
                    builder.append('.');
                else if (map[i][j] instanceof Berry)
                    builder.append('B');
                else if (map[i][j] instanceof SnakeCell)
                    builder.append('S');
            builder.append('\n');
        }
        return builder.toString();
    }
}
